# pip install google-generativeai
# https://status.cloud.google.com/

import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """

porque tive o erro 
"Traceback (most recent call last):
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py", line 467, in _make_request
    self._validate_conn(conn)
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py", line 1099, in _validate_conn
    conn.connect()
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connection.py", line 653, in connect
    sock_and_verified = _ssl_wrap_socket_and_match_hostname(
                        
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connection.py", line 806, in _ssl_wrap_socket_and_match_hostname
    ssl_sock = ssl_wrap_socket(
               
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\util\ssl_.py", line 465, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
               
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\util\ssl_.py", line 509, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
           
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\ssl.py", line 1042, in _create
    self.do_handshake()
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\ssl.py", line 1320, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py", line 793, in urlopen
    response = self._make_request(
               
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py", line 491, in _make_request
    raise new_e
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\adapters.py", line 667, in send
    resp = conn.urlopen(
           
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py", line 847, in urlopen
    retries = retries.increment(
              
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\util\retry.py", line 515, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.amazon.com.br', port=443): Max retries exceeded with url: /s?k=controle+xbox+series+x/s+com+cabo (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\e610098\Desktop\LifeHacksCode\Python\gemini_1.5_api\test.py", line 40, in <module>
    produto_encontrado = encontrar_produto_amazon(nome_produto)
                         
  File "C:\Users\e610098\Desktop\LifeHacksCode\Python\gemini_1.5_api\test.py", line 22, in encontrar_produto_amazon
    response = requests.get(url, headers=headers)
               
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
           
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        
  File "C:\Users\e610098\AppData\Local\Programs\Python\Python312\Lib\site-packages\requests\adapters.py", line 698, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='www.amazon.com.br', port=443): Max retries exceeded with url: /s?k=controle+xbox+series+x/s+com+cabo (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')))"

"""

response = model.generate_content(prompt)

print(response.text)

# using System;
# using System.Drawing;
# using Tesseract;

# namespace ImageToText
# {
#     class Program
#     {
#         static void Main(string[] args)
#         {
#             // Caminho da imagem
#             string imagePath = "caminho/para/sua/imagem.jpg";

#             // Inicializar o motor Tesseract
#             using var engine = new TesseractEngine(@"./tessdata", "eng", EngineMode.Default);

#             // Carregar a imagem
#             using var image = new Bitmap(imagePath);

#             // Reconhecer texto
#             using var page = engine.Process(image);
#             string text = page.GetText();

#             // Mostrar o texto reconhecido
#             Console.WriteLine(text);
#         }
#     }
# }