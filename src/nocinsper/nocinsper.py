import requests
from bs4 import BeautifulSoup
import pandas as pd

def noc_download_month(username, password, mes, ano, codfuncionario):
  """Pega calendário do mês e ano especificados"""
  u = f'https://noc.insper.edu.br/ControleAlocacao/calendarioprofessordetalhe.aspx?Mes={mes}&codfuncionario={codfuncionario}&ano={ano}'
  r = requests.get(u, auth = (username, password))
  soup = BeautifulSoup(r.text, 'html.parser')
  # search by id
  calend = soup.find(id='Calendar1')
  # all td with valign='top'
  all_td = calend.find_all('td', {'valign': 'top', 'align': 'left'})
  textos = [x.get_text('\n') for x in all_td]
  return textos

def noc_parse_month_el(txt):
  """Parseia calendário do mês e ano especificados"""
  # break by \n
  txt = txt.split('\n')
  if len(txt) > 1:
    events = txt[1:]
  else:
    events = ['-']
  day = [txt[0]] * len(events) # repeat day for each event
  df = pd.DataFrame({'day': day, 'event': events}) # create dataframe
  df = df[df.event != '-']
  return df

def noc_parse_month(txt):
  dfs = []
  for t in txt:
    dfs.append(noc_parse_month_el(t))
  return pd.concat(dfs)

def noc_get_month(username, password, mes, ano, codfuncionario):
  """Pega calendário do mês e ano especificados"""
  txt = noc_download_month(username, password, mes, ano, codfuncionario)
  df = noc_parse_month(txt)
  df = df.assign(month=mes, year=ano)
  return df

def noc_get_year(username, password, ano = 2024, codfuncionario = 2756):
  """Pega calendário do ano especificado.
  O ano deve ser um inteiro de 4 dígitos.
  O código do funcionário é o código do professor no sistema da insper.

  Parameters
  ----------
  username : str
    Username do sistema da insper.
  password : str
    Password do sistema da insper.
  ano : int, optional
    Ano do calendário, by default 2024
  codfuncionario : int, optional
    Código do funcionário, by default 2756

  Returns
  -------
  pd.DataFrame
    Dataframe com o calendário do ano especificado.

  Examples
  --------
  >>> noc_get_year('username', 'password', 2024, 2756)
  """
  dfs = []
  for mes in range(1, 13):
    # print message
    print(f'Getting month {mes}')
    dfs.append(noc_get_month(username, password, mes, ano, codfuncionario))
  df = pd.concat(dfs)
  return df

