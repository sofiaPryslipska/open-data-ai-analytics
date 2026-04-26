import os
import json
import pandas as pd
from flask import Flask, render_template, send_from_directory
from sqlalchemy import create_engine
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

@app.route('/')
def index():
    db_url = "postgresql://admin:secretpassword@db:5432/analytics_db"

    try:
        engine = create_engine(db_url)
        df = pd.read_sql("SELECT * FROM raw_payments LIMIT 10", engine)
        data_table = df.to_html(classes="table table-bordered table-sm", index=False)
    except Exception as e:
        data_table = f"<p>Error loading data: {e}</p>"

    try:
        with open('/shared/quality_report.txt', 'r') as f:
            quality_report = f.read()
    except FileNotFoundError:
        quality_report = "Quality report not found."

    try:
        with open('/shared/research_report.json', 'r') as f:
            research_data = json.load(f)
    except FileNotFoundError:
        research_data = {}

    return render_template('index.html',
                           table=data_table,
                           quality=quality_report,
                           research=research_data)


@app.route('/plots/<filename>')
def serve_plot(filename):
    return send_from_directory('/shared/plots', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)