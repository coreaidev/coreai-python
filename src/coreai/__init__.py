from google.colab import widgets
from IPython.display import Javascript
import ipywidgets
from IPython.display import clear_output
import requests
import threading
import time
import cloudpickle

import urllib
import urllib.request

import uuid as _uuid

import IPython as _IPython
import six as _six

from google.colab import output as _output

import cv2
import numpy

__version__ = "0.0.1"

class UsersExposingDatasets:
    def __init__(self, environment):
        self._environment = environment
    def __getattr__(self, username):
        return Datasets(self._environment, username)

class UsersExposingModels:
    def __init__(self, environment):
        self._environment = environment
    def __getattr__(self, username):
        return Models(self._environment, username)

class Datasets:
    def __init__(self, environment, username):
        self._environment = environment
        self._username = username
    def __getattr__(self, key):
        if not self._environment.is_active:
          raise Exception("Environment is not active.  Ensure you have invoked environment.activate()")
        try:
          return cloudpickle.load(urllib.request.urlopen("https://api.coreai.dev/dataset?environment=%s&owner=%s&name=%s" % (str(self._environment.sandbox_id), self._username, key)))
        except:
          raise PermissionError("Access is denied to dataset: %s.%s" % (self._username, key))


class Models:
    def __init__(self, environment, username):
        self._environment = environment
        self._username = username
    def __getattr__(self, key):
        if not self._environment.is_active:
          raise Exception("Environment is not active.  Ensure you have envoked environment.activate()")
        raise PermissionError("Access is denied to model: %s.%s" % (self._username, key))


class Environment():
  def __init__(self):
    self.sandbox_id = _uuid.uuid4()
    self.datasets = UsersExposingDatasets(self)
    self.models = UsersExposingModels(self)
    self.is_active = False
  def activate(self):
    """Renders widget to upload local (to the browser) files to the kernel.
    Blocks until the files are available.
    Returns:
      A map of the form {<filename>: <file contents>} for all uploaded files.
    """
    sandbox_id = str(self.sandbox_id)
    ui_id = str(_uuid.uuid4())

    _IPython.display.display(
        _IPython.core.display.HTML("""
      <input type="button" id="activatebutton-{ui_id}" onclick="window.open('https://www.coreai.dev/activate?uuid={sandbox_id}','targetWindow','toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=yes,width=500,height=500'); return false;" style="display: none; color: #FFFFFF; background-color: #2196F3; padding-left: 10px; padding-right: 10px; padding-top: 0px; padding-bottom: 0px; display: inline-block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: center; font-size: 13px; cursor: pointer; height: 28px; line-height: 28px; box-shadow: none; border-color: #E0E0E0; user-select: none; display: none;" value="Click to Activate Sandbox!" />
      <output id="result-{ui_id}">
        Sandbox activation button is only available when the cell has been executed in the
        current browser session. Please rerun this cell to enable button.
        </output>
      <button id="cancelbutton-{ui_id}" onclick="markCanceled();" style="display: none;">Cancel activation</button>

        <script>sandbox_id={sandbox_id}</script>
  """.format(sandbox_id=sandbox_id, ui_id=ui_id)+staticScript()))

    _output.eval_js(
        '_showActivationButton("{sandbox_id}", "{ui_id}")'.format(
            sandbox_id=sandbox_id, ui_id=ui_id))
    is_ui_active = not self.is_active
    while is_ui_active:
      time.sleep(1)
      result = _output.eval_js(
          '_checkIsActive("{sandbox_id}", "{ui_id}")'.format(
            sandbox_id=sandbox_id, ui_id=ui_id))
      if(result == 'activated'):
        self.is_active = True
        is_ui_active = False
      if(result == 'canceled'):
        is_ui_active = False
    if self.is_active:
      _output.eval_js(
          'markDone("{sandbox_id}", "{ui_id}")'.format(
            sandbox_id=sandbox_id, ui_id=ui_id))


from enum import Enum

class EnvironmentType(Enum):
    GOOGLE_COLAB = 1

class CoreAI():
   @staticmethod
   def create_environment(environment_type, resource_limit):
     return Environment()

def staticScript():
    return """
          <script>

function _showActivationButton(sandboxId, uiId) {
  const button = document.getElementById('activatebutton-'+uiId);
  button.style.display = 'inline-block';

  const outputElement = document.getElementById('result-'+uiId);
  outputElement.innerHTML = '';
  outputElement.status = 'showing-button'

  const cancel = document.getElementById('cancelbutton-'+uiId)
  cancel.onclick = () => { markCanceled(sandboxId, uiId) };
  cancel.style.display = 'inline-block';
}


function _checkIsActive(sandboxId, uiId) {
      const outputElement = document.getElementById('result-'+uiId);
      const xhr = new XMLHttpRequest();
      const url = "https://api.coreai.dev/activate?uuid="+sandboxId;

      xhr.open("GET", url);
      xhr.onreadystatechange = () => {
        console.log(sandboxId)
        console.log(xhr.responseText)
        if(xhr.responseText.includes('active')) {
          outputElement.status = 'activated'
        }
      };
      xhr.send();
      return outputElement.status;
}

function markDone(sandboxId, uiId) {
      const outputElement = document.getElementById('result-'+uiId);
      outputElement.innerHTML = 'Your environment has been successfully activated!';
    document.getElementById('cancelbutton-'+uiId).style.display = 'none';
    document.getElementById('activatebutton-'+uiId).style.display = 'none';
}

function markCanceled(sandboxId, uiId) {
    const outputElement = document.getElementById('result-'+uiId);
    outputElement.innerHTML = 'Operation canceled!  Please rerun this cell to enable the activation button.';
    outputElement.status = 'canceled'
    document.getElementById('cancelbutton-'+uiId).style.display = 'none';
    document.getElementById('activatebutton-'+uiId).style.display = 'none';
}

        </script>
    """
