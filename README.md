# Taskmaster - Gerenciador de Processos com Controle via Shell

O Taskmaster é um projeto inspirado no [Supervisor](http://supervisord.org/index.html). O principal objetivo do Taskmaster é desenvolver um daemon capaz de gerenciar subprocessos, oferecendo uma interface de controle shell para que o usuário possa monitorar e interagir com esses processos de maneira eficiente. O daemon também deve ser capaz de manipular configurações dinamicamente e registrar eventos importantes, como falhas e reinicializações de processos. Este projeto foi desenvoolvido seguiindo a arquiitetura cliente <-> servidor, onde o papel do serviidor é realizado pelo **Taskmasterd** e o cliente é realizado pelo **TaskmasterCLT**.

## Principais Funcionalidades
- Iniciar processos como subprocessos e mantê-los rodando, reiniciando-os automaticamente se necessário.
- Monitorar o status dos processos, garantindo que o daemon saiba, em tempo real, se os processos estão ativos ou não.
- Reiniciar processos conforme as condições especificadas no arquivo de configuração.
- Receber sinais para atualizar a configuração ou encerrar o daemon de forma controlada.
- Registrar eventos em logs para auditoria e depuração.


## Comandos de Controle
O Taskmaster fornece uma interface shell com os seguintes comandos:

- status: Mostra o estado de todos os processos configurados, informando se estão rodando ou parados.
- start: Inicia um ou mais processos definidos no arquivo de configuração.
- stop: Encerra um ou mais processos de forma controlada.
- restart: Reinicia processos, interrompendo-os e iniciando-os novamente.
- reload: Recarrega o arquivo de configuração durante a execução do Taskmaster, aplicando mudanças sem interromper processos que não foram alterados.
- exit: Encerra o daemon Taskmaster e todos os processos supervisionados.

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
 
_OBS: Coomo nenhum campo dentro da seção taskmaster é obrigatório  essa seçãoo pode existir ou não_ 
