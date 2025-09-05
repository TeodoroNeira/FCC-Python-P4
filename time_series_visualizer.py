import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Criação de uma lista com os meses dos anos, tanto na forma completa quanto na abreviada
# Essas listas são usadas nos gráficos, e são importantes para que os testes passem

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data

# Limpagem dos dados, conforme os requisitos do enunciado. Os filtros são os mesmos do terceiro projeto.
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot

    fig = plt.figure(figsize=(20,5)) # Define o tamanho da figura
    plt.plot(df.index, # Eixo X do gráfico
              df['value'], # Eixo Y do gráfico 
              color='red ') # Coloração do gráfico conforme o exemplo
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019') # Título
    plt.xlabel('Date') # Legenda do eixo X
    plt.ylabel('Page Views') # Legenda do eixo Y

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    ## Agrupamento pelos meses e anos, e depois faz a média dos valores. O .unstack() é para deixar os meses como colunas, e os anos como índices.
    df_bar = df.groupby([df.index.year, df.index.month])['value'].mean().unstack()

    # Draw bar plot
    
    ## Define o gráfico como do tipo barra, o tamanho e configura ele como imagem para ser salvo futuramente
    fig = df_bar.plot(kind='bar', figsize=(10,7)).get_figure()
    plt.xlabel('Years') ## Legenda do eixo X
    plt.ylabel('Average Page Views') ## Legenda do eixo Y
    plt.legend(title='Months', labels=months) ## Legenda do gráfico, com título e os meses na forma completa

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    ## Criação dos dois gráficos. Como eles precisam ficar lado a lado em uma única figura, conforme o exemplo, a função plt.subplots() é utilizada.
    fig, axes = plt.subplots(1, 2, figsize=(15,5))
    sns.boxplot(
        x='year', # Eixo X é o ano
        y ='value', # Eixo Y é o valor
        data = df_box, # Dataframe com as informações
        ax = axes[0] # Define o gráfico como o primeiro eixo (aquele que fica na esquerda)
    )
    axes[0].set_title('Year-wise Box Plot (Trend)') # Título do gráfico da esquerda
    axes[0].set_xlabel('Year') # Legenda do eixo X do gráfico da esquerda
    axes[0].set_ylabel('Page Views') # Legenda do eixo Y do gráfico da esquerda

    sns.boxplot(
        x='month', # Eixo X é o mês
        y='value', # Eixo Y é o valor
        data=df_box, # Dataframe com as informações
        order=months_short, # Define a ordem dos meses, utilizando a lista criada no início do arquivo
        ax=axes[1] # Define o gráfico como o segundo eixo (aquele que fica na direita)
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)') # Título do gráfico da direita
    axes[1].set_xlabel('Month') # Legenda do eixo X do gráfico da direita
    axes[1].set_ylabel('Page Views') # Legenda do eixo Y do gráfico da direita

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
