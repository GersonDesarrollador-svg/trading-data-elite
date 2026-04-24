from flask import Flask, render_template_string, request
import csv
import os
from datetime import datetime

app = Flask(__name__)

ARCHIVO = "data/trades.csv"
COLUMNAS = [
    "fecha","activo","direccion","entrada","stop_loss","take_profit",
    "resultado","rr_obtenido","setup","sesion",
    "ley_ema","ley_cierre","ley_espacio","ley_scanner","ley_stop",
    "emocional","notas"
]

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNAS)

FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Diario de Trades</title>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #0f0f13; color: #e0e0e0; min-height: 100vh; padding: 30px 20px; }
        .container { max-width: 620px; margin: 0 auto; background: #1a1a24; border-radius: 12px; padding: 24px; border: 1px solid #2a2a3a; }
        h2 { color: #4da6ff; border-bottom: 1px solid #2a2a3a; padding-bottom: 12px; margin-bottom: 4px; font-size: 20px; }
        .subtitulo { font-size: 11px; color: #666; margin-bottom: 20px; margin-top: 4px; }
        .seccion { font-size: 10px; font-weight: bold; color: #555; text-transform: uppercase; letter-spacing: 1px; margin: 20px 0 10px; border-top: 1px solid #2a2a3a; padding-top: 14px; }
        label { display: block; font-size: 12px; color: #aaa; margin-bottom: 4px; }
        input, select, textarea { width: 100%; padding: 9px 11px; background: #12121a; border: 1px solid #2a2a3a; border-radius: 7px; color: #e0e0e0; font-size: 13px; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #4da6ff; }
        select option { background: #1a1a24; }
        .fila { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
        .fila3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; }
        .grupo { margin-bottom: 0; }
        .btn-guardar { background: #185FA5; color: white; border: none; padding: 13px; width: 100%; border-radius: 8px; font-size: 14px; font-weight: bold; cursor: pointer; margin-top: 20px; }
        .btn-guardar:hover { background: #4da6ff; }
        .exito { background: #0d2b1a; color: #4caf82; padding: 12px 16px; border-radius: 8px; margin-bottom: 18px; font-size: 13px; border: 1px solid #1a4a30; }
        textarea { resize: vertical; min-height: 70px; }
        .ley-box { background: #12121a; border: 1px solid #2a2a3a; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; }
        .ley-titulo { font-size: 11px; color: #4da6ff; font-weight: bold; margin-bottom: 6px; }
        .hint { font-size: 11px; color: #555; margin-top: 4px; }
    </style>
</head>
<body>
<div class="container">
    <h2>📓 Diario de Trades — Elite</h2>
    <div class="subtitulo">XAUUSD · Nasdaq · Método Scanner IA + Fibonacci</div>

    {% if guardado %}
    <div class="exito">✅ Trade guardado — {{ fecha }}</div>
    {% endif %}

    <form method="POST">
        <div class="seccion">Información del trade</div>
        <div class="fila">
            <div class="grupo"><label>Activo</label>
                <select name="activo">
                    <option>XAUUSD (Oro) M5</option>
                    <option>Nasdaq NQ M1</option>
                    <option>Nasdaq MNQ M1</option>
                </select></div>
            <div class="grupo"><label>Dirección</label>
                <select name="direccion">
                    <option>Long</option>
                    <option>Short</option>
                </select></div>
        </div>
        <div class="fila3">
            <div class="grupo"><label>Entrada</label><input name="entrada" placeholder="2334.50" required/></div>
            <div class="grupo"><label>Stop Loss</label><input name="stop_loss" placeholder="2320.00" required/></div>
            <div class="grupo"><label>Take Profit</label><input name="take_profit" placeholder="2363.00" required/></div>
        </div>
        <div class="fila">
            <div class="grupo">
                <label>Resultado ($)</label>
                <input name="resultado" placeholder="Ej: 374.80 o -150.00" required/>
                <div class="hint">Ganancia: 374.80 · Pérdida: -150.00</div>
            </div>
            <div class="grupo"><label>R:R obtenido</label><input name="rr_obtenido" placeholder="2.1" required/></div>
        </div>

        <div class="seccion">Setup y sesión</div>
        <div class="fila">
            <div class="grupo"><label>Setup principal</label>
                <select name="setup">
                    <optgroup label="XAUUSD M5">
                        <option>Fibo 38.2% + EMA 200</option>
                        <option>Fibo 50% + EMA 200</option>
                        <option>Fibo 61.8% + EMA 200</option>
                        <option>Scanner IA + Rechazo Vela</option>
                    </optgroup>
                    <optgroup label="Nasdaq M1">
                        <option>Fibo 61.8% + Scanner IA</option>
                        <option>Fibo 78.6% + Trampa Liquidez</option>
                        <option>Orden Limitada 61.8%</option>
                    </optgroup>
                    <option>Otro</option>
                </select></div>
            <div class="grupo"><label>Sesión</label>
                <select name="sesion">
                    <option>NY Open 9:30-10:30</option>
                    <option>NY Mid 10:30-11:00</option>
                    <option>London</option>
                    <option>New York</option>
                    <option>Asia</option>
                </select></div>
        </div>

        <div class="seccion">Checklist — Las 5 Leyes</div>

        <div class="ley-box">
            <div class="ley-titulo">Ley 1 — EMA 200</div>
            <select name="ley_ema">
                <option value="SI">✅ Sí — precio del lado correcto</option>
                <option value="NO">❌ No — violé esta ley</option>
            </select>
        </div>

        <div class="ley-box">
            <div class="ley-titulo">Ley 2 — Cierre de vela</div>
            <select name="ley_cierre">
                <option value="SI">✅ Sí — esperé el cierre</option>
                <option value="NO">❌ No — entré antes del cierre</option>
            </select>
        </div>

        <div class="ley-box">
            <div class="ley-titulo">Ley 3 — Zona Fibonacci válida</div>
            <select name="ley_espacio">
                <option value="SI">✅ Sí — había confluencia Fibo</option>
                <option value="NO">❌ No — precio estaba en el aire</option>
            </select>
        </div>

        <div class="ley-box">
            <div class="ley-titulo">Ley 4 — Flecha del Scanner IA</div>
            <select name="ley_scanner">
                <option value="SI">✅ Sí — flecha confirmada</option>
                <option value="NO">❌ No — entré sin señal</option>
            </select>
        </div>

        <div class="ley-box">
            <div class="ley-titulo">Ley 5 — Stop Loss colocado</div>
            <select name="ley_stop">
                <option value="SI">✅ Sí — SL en el fractal</option>
                <option value="NO">❌ No — operé sin SL</option>
            </select>
        </div>

        <div class="seccion">Estado emocional</div>
        <div class="grupo" style="margin-bottom:12px">
            <select name="emocional">
                <option value="Confiado">😊 Confiado — seguí el plan</option>
                <option value="Neutral">😐 Neutral — operé mecánicamente</option>
                <option value="Ansioso">😰 Ansioso — dudé antes de entrar</option>
                <option value="FOMO">🤯 FOMO — entré por miedo a perderme el movimiento</option>
                <option value="Revenge">😤 Revenge Trading — entré para recuperar pérdida</option>
            </select>
        </div>

        <div class="grupo"><label>Notas del trade</label>
            <textarea name="notas" placeholder="¿Qué confluencias viste? ¿Qué mejorarías?"></textarea>
        </div>

        <button class="btn-guardar" type="submit">💾 Guardar Trade</button>
    </form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def diario():
    guardado = False
    fecha = ""
    if request.method == "POST":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                fecha,
                request.form["activo"],
                request.form["direccion"],
                request.form["entrada"],
                request.form["stop_loss"],
                request.form["take_profit"],
                request.form["resultado"],
                request.form["rr_obtenido"],
                request.form["setup"],
                request.form["sesion"],
                request.form["ley_ema"],
                request.form["ley_cierre"],
                request.form["ley_espacio"],
                request.form["ley_scanner"],
                request.form["ley_stop"],
                request.form["emocional"],
                request.form["notas"]
            ])
        guardado = True
    return render_template_string(FORM, guardado=guardado, fecha=fecha)

if __name__ == "__main__":
    app.run(debug=True, port=5000)