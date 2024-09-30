# Taskmaster - Gerenciador de Processos com Controle via Shell

O Taskmaster é um projeto inspirado no [Supervisor](http://supervisord.org/index.html). O principal objetivo do Taskmaster é desenvolver um daemon capaz de gerenciar subprocessos, oferecendo uma interface de controle shell para que o usuário possa monitorar e interagir com esses processos de maneira eficiente. O daemon também deve ser capaz de manipular configurações dinamicamente e registrar eventos importantes, como falhas e reinicializações de processos. Este projeto foi desenvoolvido seguiindo a arquiitetura cliente <-> servidor, onde o papel do serviidor é realizado pelo **Taskmasterd** e o cliente é realizado pelo **TaskmasterCLT**.

## Principais Funcionalidades
- Iniciar processos como subprocessos e mantê-los rodando, reiniciando-os automaticamente se necessário.
- Monitorar o status dos processos, garantindo que o daemon saiba, em tempo real, se os processos estão ativos ou não.
- Reiniciar processos conforme as condições especificadas no arquivo de configuração.
- Receber sinais para atualizar a configuração ou encerrar o daemon de forma controlada.
- Registrar eventos em logs para auditoria e depuração.

## Arquivo de Configuração
O Taskmaster usa um arquivo de configuração que define como os processos devem ser gerenciados, especificando comandos, número de processos, reinício automático, sinais de término e opções como redirecionamento de saída e variáveis de ambiente.

Exemplo de configuração:

```yaml
taskmaster:
  logfile: ./logs/taskmasterd.log
  email: "example@gmail.com"
  uid: "user"
  gid: "user"
programs:
  teste:
    cmd: "/home/user/Desktop/taskmaster/exec_teste/teste"
    numprocs: 1
    umask: 022
    workingdir: /home/user/Desktop/taskmaster
    autostart: true
    autorestart: false
    exitcodes:
      - 0
      - 2
    startretries: 3
    starttime: 5
    stopsignal: TERM
    stoptime: 10
    stdout: /home/user/Desktop/taskmaster/logs/teste.out.log
    stderr: /home/user/Desktop/taskmaster/logs/teste.err.log
    env:
      STARTED_BY: taskmaster
      ANSWER: "42"
```

Dentro de um arquivo de configuração do Taskmaster temos dois campos principais: O "**taskmaster**" e o "**proograms**".

### Seção "Taskmaster"

Na seção **taskmaster** podemos inserir os seguintes campos:

- **logfile**:
    - descrição: Este campo informa ao programa onde esta o arquiivo de logs do serrvidor  e caso esse campoo seja inserido no arquivo de coonfiguração será posiivel verificar todos oos logs peloo browser noo endereço http://localhost:4242/logs; 
    - obrigatório: NÃO
    - tipo de valor: string


- **email**:
    - descrição: O endereço de email que recebera os alertas do servidor de situações vistas como criticas
    - obrigatório: NÃO
    - tipo de valor: string


- **uid**:
    - descrição: representa um usuario válido no sistema em que o servidor esta hospedado. Todos os processos criados pelo servidor serão criado com as permissõoes desse usuário.
    - obrigatório: NÃO
    - tipo de valor: string


- **gid**:
    - descrição: representa um grupo válido no sistema em que o servidor esta hospedado. Todos os processos criados pelo servidor serão criado com as permissõoes desse usuário.
    - obrigatório: NÃO
    - tipo de valor: string
 
_OBS: Como nenhum campo dentro da seção taskmaster é obrigatório essa seção pode existir ou não_

### Seção "Programs"

Na seção **programs** é onde especificamos os grupos de processos. No exemplo de arquivo de configuração colocamos o nome de um grupo de processo de "**teste**", mas poderiamos chamar de qualquer outro nome. Nesta seção pode ter mais de um grupo. Os campos que poodem ser inseridos dentroo de um grupo de processo são os seguintes:


- **cmd**:
    - descrição: representa o comando a ser usado para iniciar o processo
    - obrigatório: SIM
    - tipo de valor: string

- **numprocs**:
    - descrição: representa o numero de processos que tem que ser iniciado com o **cmd**
    - obrigatório: NÃO
    - tipo de valor: integer
 
- **umask**:
    - descrição: representa as permissões que o processo criado terá 
    - obrigatório: NÃO
    - tipo de valor: integer

- **workingdir**:
    - descrição: representa o path raiz do projeto 
    - obrigatório: NÃO
    - tipo de valor: string
 
- **autostart**:
    - descrição: esse campo especifica se o processo será iniciado de forma automática ou não
    - obrigatório: NÃO
    - tipo de valor: boolean

- **autorestart**:
    - descrição: esse campo especifica se o processo será reiniciado de forma automatica ou não. Os valores que esse campo pode receber são true, false e "unexpected". 
    - obrigatório: NÃO
    - tipo de valor: boolean | string

- **exitcodes**:
    - descrição: são os codigos de saida doo processo que são considerado como normais, qualquer outro codiigo de saida que o processo tiver vai ser considerado como inesperado (ou "unexpcted")
    - obrigatório: NÃO
    - tipo de valor: lista
 
- **startretries**:
    - descrição: representa o número de tentativas que o servidor realizará para iniciar um processo   
    - obrigatório: NÃO
    - tipo de valor: integer
 
- **starttime**:
    - descrição: representa o tempoo que um processo tem qque ficar ativo para ser considerado como um processo iniciado coom sucesso 
    - obrigatório: NÃO
    - tipo de valor: integer
 
- **stopsignal**:
    - descrição: representa o sinal que oo servidor tem que enviar para um processo para finaliza-lo de forma "graciosa"
    - obrigatório: NÃO
    - tipo de valor: string
 
- **stoptime**:
    - descrição: representa o tempo que o servidor tem que esperar após enviar o *stopsignal* para observarr se o coomando funcionou. Após esse tempo se o processo não tiver sido finalizado o servidor forçará a finalização de forma "bruta".
    - obrigatório: NÃO
    - tipo de valor: integer
 
- **stdout**:
    - descrição: representa o path do arquivo que recebera o stdout do processo criado
    - obrigatório: NÃO
    - tipo de valor: string
 
- **stderr**:
    - descrição: representa o path do arquivo que recebera o stderr do processo criado
    - obrigatório: NÃO
    - tipo de valor: string
 
- **env**:
    - descrição: representa as variáveis de ambiente que tem que ser criadas no ambiente do processo
    - obrigatório: NÃO
    - tipo de valor: dict
 

## Taskmasterd

O Taskmasterd é um daemon criado para gerenciar processos em sistemas nix-like (Linux, Unix, etc.). Ele facilita o monitoramento e controle de vários processos em segundo plano, automatizando o gerenciamento de tarefas ou serviços. Aqui estão algumas das suas principais funcionalidades:

- Iniciar, parar e reiniciar processos automaticamente – O Taskmasterd pode ser configurado para iniciar processos automaticamente na inicialização do sistema, reiniciar processos se eles falharem e parar processos conforme necessário.
- Gerenciamento de logs – Ele captura e armazena os logs dos processos que gerencia, facilitando a depuração e a manutenção.
- Monitoramento de processos – O Taskmasterd monitora os processos e pode reiniciar automaticamente um processo se ele falhar ou travar.

Para executar o servidor estando na raiz doo projeto é só executar o seguinte comando: 

```python3 Taskmasterd/taskmasterd.py ./configs/default.yaml```

O segundo parâmetro passado no comando acima representa o path do arquivo de configuração a ser executado. Caso queira executar o servidor e mante-lo atiivo no terminal usado no momento pode executar da seguinte forma:

```python3 Taskmasterd/taskmasterd.py ./configs/default.yaml --no-daemon```

## TaskmasterCLT

O TaskmasterCLT é a ferramenta de linha de comando que acompanha o Taskmasterd, permitindo aos usuários interagir com o daemon para gerenciar os processos configurados. Através do TaskmasterCLT, você pode emitir comandos para controlar os processos monitorados pelo Taskmasterd.

Aqui estão algumas das funcionalidades do TaskmasterCLT:

- Iniciar, parar e reiniciar processos – Você pode iniciar, parar ou reiniciar processos específicos ou todos os processos gerenciados pelo Taaskmasterd usando comandos simples.
- Verificar o status dos processos – Com o TaskmasterCLT, é possível listar todos os processos monitorados e ver o status de cada um (ex.: running, stopped, starting, etc.).
- forçar a releitura do arrquivo de configuração e passar um novo arquivo de confiiguração
- Desligar o servidor

Parra iniciar o TaskmasterCLT basta executar o seguinte comando a partir da raiz do projeto:

```python3 TaskmasterCLT/taskmasterclt.py ```


### Comandos de Controle
O Taskmaster fornece uma interface shell com os seguintes comandos:

- status: Mostra o estado de todos os processos configurados, informando se estão rodando ou parados.
- start: Inicia um ou mais processos definidos no arquivo de configuração.
- stop: Encerra um ou mais processos de forma controlada.
- restart: Reinicia processos, interrompendo-os e iniciando-os novamente.
- reload: Recarrega o arquivo de configuração durante a execução do Taskmaster, aplicando mudanças sem interromper processos que não foram alterados.
- reread: recarrega o arquivo igual o reload mas diferente do reload só muda as configurações após executar o update.
- update: altera as configurações de acordo com o reread.
- exit: Encerra o daemon Taskmaster e todos os processos supervisionados.
- shutdown: Encerra o Taskmasterd

