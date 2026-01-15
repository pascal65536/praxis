unit Unit1;

interface
uses
  Winapi.Windows, Winapi.Messages, System.Variants, Vcl.Graphics,
  IdHash, IdHashSHA, Clipbrd,
  System.SysUtils, System.Classes, System.Hash,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls;

type
  TFormMain = class(TForm)
    ButtonCopy: TButton;
    ButtonCreate: TButton;
    EditPhrase: TEdit;
    EditPassword: TEdit;
    procedure ButtonCopyClick(Sender: TObject);
    procedure ButtonCreateClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  FormMain: TFormMain;
  IniFilePath: string;


implementation

{$R *.dfm}

function GetCurrentUserName: string;
const
  MaxUserNameLen = 254;
var
  UserName: array[0..MaxUserNameLen] of Char;
  Size: DWORD;
begin
  Size := MaxUserNameLen + 1;
  if GetUserName(UserName, Size) then
    Result := Copy(UserName, 1, Size - 1)
  else
    Result := '';
end;

function GetStringSha256Hash(const Text: string; Encoding: TEncoding = nil): TBytes;
var
  Stream: TStream;
begin
  if Encoding = nil then
    Encoding := TEncoding.UTF8;
  Stream := TStringStream.Create(Text, Encoding);
  try
    Result := THashSHA2.GetHashBytes(Stream);
  finally
    Stream.Free;
  end;
end;

procedure TFormMain.ButtonCopyClick(Sender: TObject);
begin
  Clipboard.AsText := EditPassword.Text; // Копируем в буфер обмена
  Close;
end;

procedure TFormMain.ButtonCreateClick(Sender: TObject);
const
  Alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\()*+,-./:;<=>?@[\]^_`{|}~ ';
var
  InputStr: string;
  IniFile: TextFile;
  HashBytes: TBytes;
  i: Integer;
  ResultStr: string;
begin

  InputStr := GetCurrentUserName() + LowerCase(Trim(EditPhrase.Text));
  HashBytes := GetStringSha256Hash(InputStr, TEncoding.UTF8);
  ResultStr := '';
  for i := 0 to 15 do
    ResultStr := ResultStr + Alphabet[(HashBytes[i] mod Length(Alphabet)) + 1];
  EditPassword.Text := ResultStr;
end;


end.

