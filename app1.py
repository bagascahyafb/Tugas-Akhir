from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder="templates")
app.secret_key = 'secret_key'

# Fungsi untuk mendapatkan catatan dari sesi pengguna atau membuat sesi baru jika belum ada
def get_user_notes():
    if 'notes' not in session:
        session['notes'] = []
    return session['notes']

# Rute untuk halaman utama
@app.route('/')
def index():
    notes = get_user_notes()
    return render_template('index1.html', notes=notes)

# Rute untuk menambah catatan baru
@app.route('/add_note', methods=['POST'])
def add_note():
    notes = get_user_notes()
    new_note = request.form.get('new_note')
    notes.append(new_note)
    session['notes'] = notes

    # Menyimpan catatan dalam berkas teks
    with open('notes.txt', 'a') as file:
        file.write(new_note + '\n')

    return redirect(url_for('index'))

# Rute untuk menghapus catatan
@app.route('/delete_note/<int:index>')
def delete_note(index):
    notes = get_user_notes()
    if 0 <= index < len(notes):
        deleted_note = notes.pop(index)
        session['notes'] = notes

        # Menyimpan catatan yang didelete dalam berkas teks
        with open('notes.txt', 'w') as file:
            for note in notes:
                file.write(note + '\n')

        # Menyimpan catatan yang didelete dalam berkas teks_deleted
        with open('notes_deleted.txt', 'a') as file_deleted:
            file_deleted.write(deleted_note + '\n')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
