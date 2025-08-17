# blognoticias
hecho por sebastian samper

#usuarios // # contraseñas
adminn // Puntotec
usernormal // Puntotec
colalbb // Puntotec

blognoticias/
├── apps/
│   ├── blog_auth/               # Gestión de usuarios, roles y permisos
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   ├── noticias/          # Noticias, comentarios, likes
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
├── templates/
│   ├── base.html
│   ├── publicaciones/
│   │   ├── post_list.html
│   │   ├── post_detail.html
│   │   └── formset_clean.html
│   └── usuarios/
│       ├── login.html
│       └── signup.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/                      # Imágenes subidas
├── scripts/                    # Validaciones previas al deploy
│   ├── check_media.py
│   ├── check_templates.py
│   └── check_users.py
├── logs/                       # Logging de errores y acciones críticas
├── manage.py
└── requirements.txt
