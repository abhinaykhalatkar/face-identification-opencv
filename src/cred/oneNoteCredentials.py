from ..oneNoteOp.onenoteauth import OneNoteAuth

authenticator = OneNoteAuth(client_id="your_client_id", 
                            client_secret="your_client_secret", 
                            redirect_url="your_redirect_url",
                            scope='office.onenote wl.signin wl.offline_access')
token = authenticator.get_token()
