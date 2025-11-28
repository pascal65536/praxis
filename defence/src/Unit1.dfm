object FormMain: TFormMain
  Left = 0
  Top = 0
  Caption = 'Shiper'
  ClientHeight = 97
  ClientWidth = 573
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object ButtonCopy: TButton
    Left = 476
    Top = 56
    Width = 75
    Height = 25
    Caption = 'Copy'
    TabOrder = 0
    OnClick = ButtonCopyClick
  end
  object ButtonCreate: TButton
    Left = 476
    Top = 16
    Width = 75
    Height = 25
    Caption = 'Create'
    TabOrder = 1
    OnClick = ButtonCreateClick
  end
  object EditPhrase: TEdit
    Left = 16
    Top = 16
    Width = 454
    Height = 23
    TabOrder = 2
    Text = 'Enter Your Phrase'
  end
  object EditPassword: TEdit
    Left = 16
    Top = 57
    Width = 454
    Height = 23
    TabOrder = 3
    Text = 'Get pasword'
  end
end
