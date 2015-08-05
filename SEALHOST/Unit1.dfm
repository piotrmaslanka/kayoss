object Form1: TForm1
  Left = 323
  Top = 180
  Align = alClient
  BorderStyle = bsNone
  Caption = 'Kamera - sealhost'
  ClientHeight = 246
  ClientWidth = 382
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
  object VideoWindow1: TVideoWindow
    Left = 0
    Top = 0
    Width = 382
    Height = 246
    FilterGraph = FilterGraph
    VMROptions.Mode = vmrWindowed
    Color = clBlack
    Align = alClient
    object Button1: TButton
      Left = 184
      Top = 16
      Width = 75
      Height = 25
      Caption = 'Button1'
      TabOrder = 0
    end
  end
  object FilterGraph: TFilterGraph
    Mode = gmCapture
    GraphEdit = True
    Left = 40
    Top = 8
  end
  object SEALFilter: TFilter
    BaseFilter.data = {
      EA00000037D415438C5BD011BD3B00A0C911CE86D60000004000640065007600
      6900630065003A0070006E0070003A005C005C003F005C007500730062002300
      7600690064005F00300061006300380026007000690064005F00630033003300
      390026006D0069005F0030003000230037002600330037003600620034006300
      6600260030002600300030003000300023007B00360035006500380037003700
      330064002D0038006600350036002D0031003100640030002D00610033006200
      39002D003000300061003000630039003200320033003100390036007D005C00
      67006C006F00620061006C000000}
    FilterGraph = FilterGraph
    Left = 72
    Top = 8
  end
  object SampleGrabber: TSampleGrabber
    OnBuffer = SampleGrabberBuffer
    FilterGraph = FilterGraph
    MediaType.data = {
      7669647300001000800000AA00389B717DEB36E44F52CE119F530020AF0BA770
      FFFFFFFF0000000001000000809F580556C3CE11BF0100AA0055595A00000000
      0000000000000000}
    Left = 8
    Top = 8
  end
  object Timer1: TTimer
    Interval = 100
    Left = 112
    Top = 8
  end
  object httpServ: TIdHTTPServer
    Active = True
    Bindings = <>
    CommandHandlers = <>
    DefaultPort = 13000
    Greeting.NumericCode = 0
    MaxConnectionReply.NumericCode = 0
    ReplyExceptionCode = 500
    ReplyTexts = <>
    ReplyUnknownCommand.NumericCode = 0
    OnCommandGet = httpServCommandGet
    Left = 144
    Top = 8
  end
end
