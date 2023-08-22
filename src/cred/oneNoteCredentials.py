
from oneNoteOp.onenoteauth import OneNoteAuth
from oneNoteOp.onenote import OneNote

authenticator = OneNoteAuth(client_id="a84beec0-3795-4acb-ba8c-3207c883c346", 
                            client_secret="Ta-8Q~YeaZImhNY6NodLtUIlzjWddvvwl-N-Ibht", 
                            redirect_url="http://localhost:8085",
                            scope='Notes.ReadWrite User.Read')

onenote_instance = OneNote(client_id="a84beec0-3795-4acb-ba8c-3207c883c346", 
                            client_secret="Ta-8Q~YeaZImhNY6NodLtUIlzjWddvvwl-N-Ibht", 
                           redirect_url="http://localhost:8085",
                           scope='Notes.ReadWrite User.Read')

token = authenticator.get_token()
