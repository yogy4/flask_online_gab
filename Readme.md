# Untuk dapat menjalankan maka ada beberapa langkah yang harus dilalui(dalam hal ini, ujicoba menggunakan os linux, python 2.7 dan database postgresql 11.3)
1. Install virtual environment dan pip (python2-virtualenv; python2-pip)
2. Masuk ke root direktori
3. Buat virtual environment(virtualenv -p /usr/bin/python2 nama_env)
4. Aktifkan virtual environment(source nama_env/bin/activate)
5. Install package pendukung dengan pip(pip install -r req.txt)
6. Buat Database di postgresql lalu set configurasi di file .env(pada export DATABASE_URI)
7. Lakukan migrasi database(python manage.py db init; python manage.py db migrate; python manage.py db upgrade)
8. Lalu jalankan(python manage.py runserver)
