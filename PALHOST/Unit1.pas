unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, DSPack, DSUtil, DirectShow9, BaseFilterEditor, ExtCtrls,
  IdBaseComponent, IdComponent, IdTCPServer, IdCustomHTTPServer,
  IdHTTPServer, StrUtils, Jpeg, IdThreadMgr, IdThreadMgrDefault,
  IdThreadMgrPool;

type
  TForm1 = class(TForm)
    FilterGraph: TFilterGraph;
    VideoWindow: TVideoWindow;
    PALFilter: TFilter;
    SampleGrabber: TSampleGrabber;
    Timer1: TTimer;
    httpServ: TIdHTTPServer;
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
  while not AFrameBMP_Ready do Sleep(20);

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
     { this is fully-deterministic, and can be used }
    { this can be invoked at any time, but to being sure that video is playing
      because it polls InternetEnabled }
    try
      SampleGrabber.GetBitmap(AFrameBMP, pBuffer, BufferLen);
      AFrameBMP_Ready := True;
    except
      Application.Terminate;
    end;
end;
{---------------------------------------}
procedure TForm1.SetupPreview;
var
 AMXBAR: IAMCrossbar; AVD: IAMAnalogVideoDecoder; IASC: IAMStreamConfig;
 CaptureGraph: ICaptureGraphBuilder2; SourceFilter: IBaseFilter;
 MediaType: PAMMediaType; MediaTypeH: PVIDEOINFOHEADER;
begin
  FilterGraph.ClearGraph; FilterGraph.Active := False;
  Devices := TSysDevEnum.Create(CLSID_VideoInputDeviceCategory);
  PALFilter.BaseFilter.Moniker := Devices.GetMoniker(0);
  FilterGraph.Active := True;
  try
    FilterGraph.QueryInterface(ICaptureGraphBuilder2, CaptureGraph);
    PALFilter.QueryInterface(IBaseFilter, SourceFilter);
    CaptureGraph.FindInterface(@LOOK_UPSTREAM_ONLY, nil, SourceFilter,
          IID_IAMCrossBar, AMXBAR);
    CaptureGraph.FindInterface(nil, nil, SourceFilter,
          IID_IAMAnalogVideoDecoder, AVD);
    CaptureGraph.FindInterface(@PIN_CATEGORY_PREVIEW, nil, SourceFilter,
          IID_IAMStreamConfig, IASC);
    AMXBAR.Route(0, 2);                   // Select: Composite
    AVD.put_TVFormat(AnalogVideo_PAL_B);  // Select: PAL B
    IASC.GetFormat(MediaType);
    MediaTypeH := MediaType.pbFormat;
    MediaType.subtype := MEDIASUBTYPE_RGB24;
    MediaTypeH.bmiHeader.biWidth := 768;
    MediaTypeH.bmiHeader.biHeight := 576;
    IASC.SetFormat(MediaType^);
    DeleteMediaType(MediaType);
  finally
    AMXBAR := nil; AVD := nil; IASC := nil; CaptureGraph := nil; SourceFilter := nil;
  end;
  with FilterGraph as ICaptureGraphBuilder2 do
  begin
     RenderStream(@PIN_CATEGORY_PREVIEW, nil, PALFilter as IBaseFilter,
                  SampleGrabber as IBaseFilter, VideoWindow as IBaseFilter);
  end;
  FilterGraph.Play;
end;
end.
