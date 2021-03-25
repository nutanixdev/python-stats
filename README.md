# Nutanix Prism VM Stats

This small demo will demonstrate how to grab a list of available VM stats, then iterate over to generate a point-in-time snapshot of what a VM is doing.

## Usage

- Recommended Python version 3.8 or later.  Testing for this script was done with Python 3.8 on Ubuntu Linux 20.04.
- Create and activate a virtual environment:

  ```
  python3.8 -m venv venv
  . venv/bin/activate
  ```

- Install the script dependencies:

  ```
  pip3 install -r requirements.txt
  ```

- Rename `.env.example` to `.env`
- Edit `.env` to match your environment requirements i.e. Prism Central and Cluster IP address & credentials

  **Note:** Because this demo uses the v3 and v1 Nutanix Prism APIs, we must submit a request first to Prism Central, then to a specific cluster; the v1 API is **not** supported on Prism Central.

- Edit `config.json` and set `required_metrics` to a quoted, comma-separated list of the metrics you'd like to look for; if you want to display all metrics, leave the `required_metrics` variable empty i.e. `""`

  **Note:** For your convenience, a list of all available VM metrics has been included in `config.json` as `available_metrics`

- Run the script:

  ```
  python ./stats.py
  ```

## Additional Info

By default, this script does not require a verified SSL connection to Prism Element or Prism Central.  If you have configured Prism Element and/or Prism Central with a valid SSL certificate and require SSL certificate verification in your environment, please comment the following line:

```
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Screenshot

![Screenshot of Python VM stats script being run](./screenshot.png?raw=true)

## Disclaimer

Please see the `.disclaimer` file that is distributed with this repository.