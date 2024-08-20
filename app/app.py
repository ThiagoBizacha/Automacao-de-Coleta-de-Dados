from flask import Flask, render_template, request, redirect, url_for
import seu_script  # Importe seu script aqui

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Execute seu script e obtenha os resultados
        result = seu_script.execute()  # Substitua `execute()` pela função do seu script
        return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
