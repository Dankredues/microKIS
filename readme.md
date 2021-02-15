# Was ist es?

Ein Frontend zur Aufnahme von Patienten und senden einer HL7 ADT Nachricht an ein Gateway. Ebenso zum Import von Trenddaten über HL7 Inbound.

## Installation

1. Erzeuge eine virtuelle Umgebung (venv) zur Entwicklung

```bash 
python -m venv path\to\microkis\venv
```



2. Mit Packetmanager benötigte Pakete installieren [pip](https://pip.pypa.io/en/stable/) 



```bash
pip install flask hl7 websockets asyncio aiorun 
```

3. In der Config File (config.py) die Server Adresse und Port des HL7 Gateways eintragen und ggf. die IN / OUTBOUND Schnittstelle deaktivieren.


4. Im Gateway des Vista120 Gateways die IP des sendenden Systemes eintragen.

![Screenshot GW](https://raw.githubusercontent.com/Dankredues/microKIS/master/gateway_settings.png)

## Start der Applikation
Aktivieren der Virtuellen Umgebung:

```
#>    .\venv\Scripts\activate.bat / activate.ps / activate

#> (venv):
```

Windows :

```bash
SET FLASK_APP=main
flask run 
```

Unix/Linux/ Mac
```bash
export FLASK_APP=main
flask run 
````


Für einen Produktivbetrieb ist der in Flask eingebaute Webserver nicht geeignet! Dafür einen WSGI kompatiblen Server einsetzen ( Gunicorn oder ähnlich).



## Verwendung

Übersichtsseite

Hier werden Patienten Aufgenommen  und Entlassen, sowie die Details aufgerufen.

![Homescreen](https://github.com/Dankredues/microKIS/raw/master/doc/homeScreen.png)

Bei der Patientenaufnahme müssen alle Felder ausgefüllt sein.
Aktuell keine Umlaute / Sonderzeichen

![Admit Patient](https://github.com/Dankredues/microKIS/raw/master/doc/admit.png)

Trendanzeige unter Details. Aktuell ohne Filter / Skalierungsmöglichkeiten

![Admit Patient](https://github.com/Dankredues/microKIS/raw/master/doc/trends2.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)