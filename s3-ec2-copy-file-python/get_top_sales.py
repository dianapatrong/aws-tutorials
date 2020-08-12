import pandas as pd

video_games_sales = pd.read_csv('video_game_sales.csv')
sales_by_platform = video_games_sales[['Platform', 'Global_Sales']].groupby(by=['Platform']).sum().sort_values(by=['Global_Sales'], ascending=False)
sales_by_platform.to_csv('sales_by_platform.csv')