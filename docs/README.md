
https://github.com/user-attachments/assets/3ce7503c-85be-4b42-ac98-60ba1ccaf73a


<br/>

- Primeira parte da execução do Bot. Nesse trecho do processo de lançamento de uma NF, o Bot está clicando no botão _Ver Documentos_ para abrir o processo no portal. Ao abrir o processo no portal, ele coleta a URL do processo e abre a mesma página no Chrome driver Selenium. Através desse acesso virtual à pagina do processo, por meio da biblioteca Selenium, é possível mapear todos os elementos html presentes na página, o que nos permite extrair a chave de acesso da NF que está sendo lançada, e, com a chave de acesso, procurarmos o arquivo xml na pasta repositório de XMLs. Caso o arquivo XML ainda não esteja na pasta, o Microsiga permite que façamos a extração do XML diretamente na rotina Processo Pagamento, como ocorreu no vídeo, onde foi passado o caminho do diretório xmlFiscalio (pasta repositório) para receber o arquivo xml do processo. Então o Bot lê o arquivo e extrai os dados conforme está no módulo _extratorXML_. Depois clica em _Dados da Nota_ para iniciar o lançamento. Após inserir a TES 408 por padrão, a primeira conferência que ele faz é a da Filial de entrega, que precisa corresponder ao CNPJ do destinatário presente na NF. Caso não corresponda, o lançamento é cancelado e aquela chave de acesso é incorporada a uma lista de processos a serem ignorados pela automação. Quem deve efetuar a correção desses processos é um operador do setor financeiro.


