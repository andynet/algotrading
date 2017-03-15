import functions

buying_prices, selling_prices = functions.read_input("EUR_USD.data")

buying_prices_local_min = functions.find_local_min(buying_prices)
selling_prices_local_max = functions.find_local_max(selling_prices)

in_position = False
position_buy_price = None
balance = 10000000

for i in range(len(buying_prices_local_min)):
    # ak su obe None preskakujem
    if buying_prices_local_min[i] == None and selling_prices_local_max[i] == None:
        continue
    # ak mam iba buying price
    if buying_prices_local_min[i] is not None:
        # ak som nasiel lepsiu vymenim
        if in_position and buying_prices_local_min[i] < position_buy_price:
            position_buy_price = buying_prices_local_min[i]
        # ak nemam ziadnu beriem
        if not in_position:
            position_buy_price = buying_prices_local_min[i]
            in_position = True
    # ak mam iba selling price
    if selling_prices_local_max[i] is not None:
        # ak som v pozicii, pohladam najblizsiu selling price vyssiu ako mam teraz a pozriem sa
        # ci medzi aktualnou a tou najblizsou je nejaky buypoint nizsi ako terajsi sellpoint
        if in_position:
            current_sellpoint = i
            # dalsia predajna pozicia, vacsia ako aktualna
            next_sellpoint = functions.find_next_sellpoint(current_sellpoint, selling_prices_local_max)
            # nakupna pozicia, mensia ako aktualna predajna medzi aktualnou predajnou a dalsou predajnou
            next_buypoint = functions.find_next_buypoint(current_sellpoint, next_sellpoint,
                                                         selling_prices_local_max, buying_prices_local_min)
            # ak neviem predat za viac tak predavam
            if next_sellpoint == None:
                position_sell_price = selling_prices_local_max[current_sellpoint]
                balance = functions.realize_order(balance, 0, position_buy_price, current_sellpoint, position_sell_price)
            # ak budem zachvilu vediet kupit za menej ako teraz mozem predat tak predavam
            if next_buypoint != None:
                position_sell_price = selling_prices_local_max[current_sellpoint]
                balance = functions.realize_order(balance, 0, position_buy_price, current_sellpoint, position_sell_price)

