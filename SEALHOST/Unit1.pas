unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, DSPack, DSUtil, DirectShow9, BaseFilterEditor, ExtCtrls,
  IdBaseComponent, IdComponent, IdTCPServer, IdCustomHTTPServer,
  IdHTTPServer, StrUtils, Jpeg, IdThreadMgr, IdThreadMgrDefault,
  IdThreadMgrPool, StdCtrls;
type
  TForm1 = class(TForm)
    FilterGraph: TFilterGraph;
    SEALFilter: TFilter;
    SampleGrabber: TSampleGrabber;
    Timer1: TTimer;
    httpServ: TIdHTTPServer;
    VideoWindow1: TVideoWindow;
    Button1: TButton;
    procedure FormCreate(Sender: TObject);
    procedure httpServCommandGet(AThread: TIdPeerThread;
      ARequestInfo: TIdHTTPRequestInfo;
      AResponseInfo: TIdHTTPResponseInfo);
    procedure SampleGrabberBuffer(sender: TObject; SampleTime: Double;
      pBuffer: Pointer; BufferLen: Integer);
  private
    { Private declarations }
  public
    procedure SetupPreview;
  end;

var
  Form1: TForm1;
  Devices: TSysDevEnum;
  AFrameBMP: TBitmap;
  AFrameBMP_Ready: Boolean;

  HTTPControl: TRTLCriticalSection;

implementation

{$R *.dfm}


procedure TForm1.FormCreate(Sender: TObject);
begin
  Form1.SetupPreview;
  ShowCursor(False);
  AFrameBMP := TBitmap.Create;
  InitializeCriticalSection(HTTPControl);
end;



procedure TForm1.httpServCommandGet(AThread: TIdPeerThread;
  ARequestInfo: TIdHTTPRequestInfo; AResponseInfo: TIdHTTPResponseInfo);
var
  RawCmd: String;
  JpegImage: TJpegImage;
begin
  EnterCriticalSection(HTTPControl);
  RawCmd := RightStr(ARequestInfo.Document, Length(ARequestInfo.Document)-1);
  AResponseInfo.ContentText := '';
  AResponseInfo.ResponseText := 'OK';
  AResponseInfo.CloseConnection := True;
  AResponseInfo.ContentType := 'text/plain';

      JpegImage := TJpegImage.Create;

        { this is fully-deterministic }
      while not AFrameBMP_Ready do begin end;
      JpegImage.Assign(AFrameBMP);
      JpegImage.ProgressiveEncoding := True;
      JpegImage.CompressionQuality := 70;
      AResponseInfo.ContentStream := TMemoryStream.Create;
      JpegImage.SaveToStream(AResponseInfo.ContentStream);
      JpegImage.Destroy;

      AResponseInfo.ContentType := 'image/jpeg';

  AResponseInfo.WriteHeader;
  AResponseInfo.WriteContent;

  LeaveCriticalSection(HTTPControl);
end;

procedure TForm1.SampleGrabberBuffer(sender: TObject; SampleTime: Double;
  pBuffer: Pointer; BufferLen: Integer);
begin
      SampleGrabber.GetBitmap(AFrameBMP, pBuffer, BufferLen);
      AFrameBMP_Ready := True;
end;
{---------------------------------------}

procedure TForm1.SetupPreview;
var
  Devices: TSysDevEnum;
  i: Integer;
begin
  FilterGraph.ClearGraph;
  FilterGraph.Active := false;
  Devices := TSysDevEnum.Create(CLSID_VideoInputDeviceCategory);
  SEALFilter.BaseFilter.Moniker := Devices.GetMoniker(1);
  FilterGraph.Active := true;
  with FilterGraph as ICaptureGraphBuilder2 do
    RenderStream(@PIN_CATEGORY_PREVIEW, nil, SEALFilter as IBaseFilter, SampleGrabber as IBaseFilter, VideoWindow1 as IbaseFilter);
  FilterGraph.Play;
end;

end.

