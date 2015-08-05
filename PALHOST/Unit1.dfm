object Form1: TForm1
  Left = 1164
  Top = 352
  Align = alClient
  BorderStyle = bsNone
  Caption = 'Kamera - palhost'
  ClientHeight = 272
  ClientWidth = 380
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  FormStyle = fsStayOnTop
  OldCreateOrder = False
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object VideoWindow: TVideoWindow
    Left = 0
    Top = 0
    Width = 380
    Height = 272
    FullScreenTopMost = True
    FilterGraph = FilterGraph
    VMROptions.Mode = vmrWindowless
    VMROptions.Preferences = []
    Color = clBlack
    Visible = False
    Align = alClient
  end
  object FilterGraph: TFilterGraph
    Mode = gmCapture
    GraphEdit = True
    Left = 80
    Top = 64
  end
  object PALFilter: TFilter
    BaseFilter.data = {00000000}
    FilterGraph = FilterGraph
    Left = 120
    Top = 64
  end
  object SampleGrabber: TSampleGrabber
    OnBuffer = SampleGrabberBuffer
    FilterGraph = FilterGraph
    MediaType.data = {
      7669647300001000800000AA00389B717DEB36E44F52CE119F530020AF0BA770
      FFFFFFFF0000000001000000809F580556C3CE11BF0100AA0055595A00000000
      0000000000000000}
    Left = 24
    Top = 56
  end
  object Timer1: TTimer
    Interval = 100
    Left = 168
    Top = 48
  end
  object httpServ: TIdHTTPServer
    Active = True
    Bindings = <>
    CommandHandlers = <>
    DefaultPort = 12000
    Greeting.NumericCode = 0
    MaxConnectionReply.NumericCode = 0
    ReplyExceptionCode = 500
    ReplyTexts = <>
    ReplyUnknownCommand.NumericCode = 0
    OnCommandGet = httpServCommandGet
    Left = 296
    Top = 56
  end
end
