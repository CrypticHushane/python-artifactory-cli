# Installation Instructions for `jfrog-pypi-trial` Package

## Prerequisites

- Ensure you have **Python** and **pip** installed on your system.
  - You can verify this by running:
    ```bash
    python --version
    pip --version
    ```
  - If pip is not installed, you can install it by running:
    ```bash
    python -m ensurepip --upgrade
    ```

## Installing the Package

To install the `jfrog-pypi-trial` package from Artifactory, follow these steps:

### Step 1: Generate Your API Key (if not already done)

If you don't have an API key yet:
1. Log into the Artifactory web UI.
2. Go to your **profile**.
3. Under **API Key**, click **Generate** to create a new key.

### Step 2: Install the Package Using pip

Run the following command to install the package:

```bash
pip install jfrog-pypi-trial --index-url https://trialnr323w.jfrog.io/artifactory/api/pypi/compuzign-oshane-pypi/simple -u <USERNAME> -p <API_KEY>
