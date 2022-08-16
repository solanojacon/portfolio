# Correlação entre Compradores e Leads / *Correlation Between Buyers and Leads*

***

## Desafio de Ciência de Dados / *Data Science Challenge*

***

### :question: Contextualização / *Contextualization*
:question:
Você trabalha em uma empresa do tipo e-commerce que vende produtos para cabelo personalizados.
Para personalizar o produto, a empresa solicita que o cliente preencha um formulário onde
irá contar sobre a sua rotina e seu cabelo. Após finalizar o preenchimento, o cliente é
direcionado automaticamente para o checkout, onde ele irá optar por fechar a compra ou não.

A experiência de venda online é baseada em três etapas:
- Preenchimento do formulário
- Seleção dos produtos
- Fechamento da compra

*You work at an e-commerce company that sells custom hair products.  
To customize the product, the company asks the customer to fill in a form where
will tell you about your routine and your hair. After completing the filling, the customer is
automatically directed to the checkout, where he will choose to close the purchase or not.*

*The online selling experience is based on three steps:*
- *Filling in the form*
- *Product selection*
- *Closing of purchase*

:bowtie:

### :exclamation: Problema e desafio / *Problem and challenge*
:exclamation:
A empresa está gastando muito dinheiro com disparos via Whatsapp para pessoas que preenchem o formulário (leads), 
desta forma seria interessante qualificar quem são os leads que possuem maior probabilidade de efetuar uma compra
e assim tornar os disparos mais efetivos.

Você então é convocado para solucionar tal desafio, e portanto deve **achar a correlação entre compradores e leads.**

Para isso, acesse o banco de dados presente em sua empresa para fazer a coleta dos dados, e use os recursos ao seu alcance para solucionar o problema e apresentar as suas conclusões.


*The company is spending a lot of money on WhatsApp shots for people who fill out the form (leads),
this way it would be interesting to qualify who are the leads that are most likely to make a purchase
and thus make the shots more effective.*

*You are then called upon to solve such a challenge, and therefore must **find the correlation between buyers and leads**.*

*To do this, access your company's database to collect data, and use the resources at your disposal to solve the problem and present your conclusions.*


### Recursos / *Resources*

Sua empresa contém um banco de dados relacional (Postgres) hospedado remotamente, com as credenciais de acesso listadas [aqui](db_access.txt). O banco contém a seguinte estrutura de tabelas e relações:

*Your company contains a remotely hosted relational database (Postgres) with the access credentials listed [here](db_access.txt). The database contains the following structure of tables and relationships:*

![Database Structure](images/db-uml.png 'Database Structure')


### :rocket: Entregas / *Deliveries*
:rocket:
> A entrega deve conter um arquivo .ipynb (Jupyter notebook) contendo toda evolução da solução, sendo que os seguintes pontos devem estar presentes:
> 1. Leitura dos dados e normalização
> 1. Separação de bases para treinar e efetuar o crossvalidation
> 1. Respaldo teórico e prático sobre as escolhas dos algoritmos (podendo ser mais de um)
> 1. Como e porquê foram escolhidas as features analisadas
> 1. Salvar o arquivo de treinamento, fazer sua leitura e gerar o score
> 1. Resultado final com métricas de acertividade do algoritmo

> *The delivery must contain an .ipynb file (Jupyter notebook) containing the entire evolution of the solution, and the following points must be present:*
> 1. *Data reading and normalization*
> 1. *Separation of bases for training and crossvalidation*
> 1. *Theoretical and practical support on the choices of algorithms (there may be more than one)*
> 1. *How and why the analyzed features were chosen*
> 1. *Save the training file, read it and generate the score*
> 1. *Final result with algorithm accuracy metrics*
