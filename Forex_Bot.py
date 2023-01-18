import time
import MetaTrader5 as mt5
import threading
import numpy
import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("FOREX BOT(XAUUSD)")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_left.grid_rowconfigure(0, minsize=10)  
        self.frame_left.grid_rowconfigure(5, weight=1) 
        self.frame_left.grid_rowconfigure(8, minsize=20)   
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="CLOSE",
                                              text_font=("Roboto Medium", -16)) 
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="CLOSE ALL",
                                                command=self.Close_All_Positions)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="  CLOSE 0.01   ",
                                                command=self.Close_Onepercent
                                                )
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="CLOSE PEND",
                                                command=self.Close_Pend
                                                )
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=("ArmagBi", mt5.__version__) ,
                                                   height=100,
                                                   corner_radius=6,
                                                   fg_color=("white", "gray10"),  
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.label_info_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=('armagbi'),
                                                   height=30,
                                                   corner_radius=10,
                                                   fg_color=("white", "gray10"), 
                                                   justify=tkinter.LEFT)
        self.label_info_2.grid(column=0, row=1, sticky="n", padx=10, pady=10)

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="OPTIONS")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1,text='AUTO      ',
                                                           command=self.Options
                                                           )
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=2,text='MANUAL',
                                                           command=self.Options
                                                           )
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,       
                                                text="RISK FREE",
                                                command=threading.Thread(target=self.Risk_Free).start
                                                )
        self.switch_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="AUTO TRADE"
                                                )
        self.switch_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                                width=5,
                                                placeholder_text="PRICE")
        self.entry.grid(row=8, column=0, columnspan=1, pady=5, padx=5, sticky="we")
        
        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                        values=["SELL","BUY"])
        self.combobox_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")
        
        self.combobox_1.bind("<<ComboboxSelected>>", self.side)
        
        self.entry_2 = customtkinter.CTkEntry(master=self.frame_right,
                                            width=5,
                                            placeholder_text="LOT")
        self.entry_2.grid(row=7, column=0, columnspan=1, pady=5, padx=5, sticky="we")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="Conection"
                                                     )
        self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="STOP",
                                                border_width=2,  
                                                fg_color=None,  
                                                command=self.Stop)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=5, padx=5, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="START",
                                                border_width=2,  
                                                fg_color=None,  
                                                command=threading.Thread(target=self.Start).start)
        self.button_5.grid(row=8, column=1, columnspan=1, pady=5, padx=5, sticky="we")

        self.optionmenu_1.set("Dark")
        self.combobox_1.set("ORDER TYPE")
        self.check_box_1.configure(state="disabled")
        #self.radio_button_1.select()







        positions = mt5.orders_get()

        def close_position(position):
            tick = mt5.symbol_info_tick(position.symbol)
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": position.ticket,
                "symbol": position.symbol,
                "type": mt5.ORDER_TYPE_BUY_STOP if position.type == 4 else mt5.ORDER_TYPE_SELL_STOP,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC
            }
            result = mt5.order_send(request)
            return result
        for position in positions:
            close_position(position)










    def Start(self):
        if self.radio_var.get()==1: # If Auto
            if not mt5.initialize():
                print('Not Connected')
                return self.Start
            else:
                print('Conected To MT5')
                self.check_box_1.select()
            print("Auto")
            symbol = ("XAUUSD")
            Volume = float(self.entry_2.get())

            def Auto_Pending(): 
                        mt5.initialize()
                        orders=mt5.orders_total()
                        pos = mt5.positions_total()

                        if orders==0:
                            Request_Auto_Pending_Buy = {
                                        "action": mt5.TRADE_ACTION_PENDING,
                                        "symbol": symbol,
                                        "volume": Volume,
                                        "type": mt5.ORDER_TYPE_BUY_STOP,
                                        "price": mt5.symbol_info_tick(symbol).ask+(30*mt5.symbol_info(symbol).point),
                                        #"sl": mt5.symbol_info_tick(symbol).ask-(70*mt5.symbol_info(symbol).point),
                                        "deviation": 20,
                                        "magic": 234000,
                                        "comment": "",
                                        "type_time": mt5.ORDER_TIME_GTC,
                                        "type_filling": mt5.ORDER_FILLING_RETURN,
                                    }
                            result_Auto_Pending = mt5.order_send(Request_Auto_Pending_Buy)
                        
                        if orders>=2:
                            #print('Pending Has Been Placed')
                            time.sleep(0.5)
                            Auto_Pending()

                        else:
                            for position in positions:
                                close_position(position)
                            orders_get=mt5.orders_get()
                            orders_get = orders_get[0]
                            ordertype=orders_get.type
                            orderprice=orders_get.price_open

                            if ordertype ==5:
                                Request_Auto_Pending_Buy = {
                                            "action": mt5.TRADE_ACTION_PENDING,
                                            "symbol": symbol,
                                            "volume": Volume,
                                            "type": mt5.ORDER_TYPE_BUY_STOP,
                                            "price": mt5.symbol_info_tick(symbol).ask+(30*mt5.symbol_info(symbol).point),
                                            #"sl": mt5.symbol_info_tick(symbol).ask-(70*mt5.symbol_info(symbol).point),
                                            "deviation": 20,
                                            "magic": 234000,
                                            "comment": "",
                                            "type_time": mt5.ORDER_TIME_GTC,
                                            "type_filling": mt5.ORDER_FILLING_RETURN,
                                        }
                                result_Auto_Pending = mt5.order_send(Request_Auto_Pending_Buy)
                                    
                            if ordertype ==4:
                                Request_Auto_Pending_Sell = {
                                            "action": mt5.TRADE_ACTION_PENDING,
                                            "symbol": symbol,
                                            "volume": Volume,
                                            "type": mt5.ORDER_TYPE_SELL_STOP,
                                            "price": mt5.symbol_info_tick(symbol).bid-(30*mt5.symbol_info(symbol).point), 
                                            #"sl": mt5.symbol_info_tick(symbol).bid+(70*mt5.symbol_info(symbol).point),   
                                            "deviation": 20,
                                            "magic": 234000,
                                            "comment": "",
                                            "type_time": mt5.ORDER_TIME_GTC,
                                            "type_filling": mt5.ORDER_FILLING_RETURN,
                                        }
                                result_Auto_Pending = mt5.order_send(Request_Auto_Pending_Sell)
                                return result_Auto_Pending                      
                                

            while True:
                    time.sleep(1)
                    result_Auto_Pending = Auto_Pending()

        if self.radio_var.get()==2: # If Manual
            mt5.initialize()
            print('Manual')
            self.check_box_1.select()
            symbol = ("XAUUSD")
            Price = float(self.entry.get())
            Volume = float(self.entry_2.get())

            if self.combobox_1.get() == 'BUY': # Buy Pending
                    Request_Pending_Buy = {
                                    "action": mt5.TRADE_ACTION_PENDING,
                                    "symbol": symbol,
                                    "volume": Volume,
                                    "type": mt5.ORDER_TYPE_BUY_STOP,
                                    "price": Price,  
                                    "sl": Price-(10*mt5.symbol_info(symbol).point),   
                                    "deviation": 20,
                                    "magic": 234000,
                                    "comment": "",
                                    "type_time": mt5.ORDER_TIME_GTC,
                                    "type_filling": mt5.ORDER_FILLING_RETURN,
                                }
                    result_Pending_Buy = mt5.order_send(Request_Pending_Buy)              

            if self.combobox_1.get() == 'SELL': # SELL Pending
                    Request_Pending_Sell = {
                                    "action": mt5.TRADE_ACTION_PENDING,
                                    "symbol": symbol,
                                    "volume": Volume,
                                    "type": mt5.ORDER_TYPE_SELL_STOP,
                                    "price": Price,  
                                    "sl": Price+(10*mt5.symbol_info(symbol).point),
                                    "deviation": 20,
                                    "magic": 234000,
                                    "comment": "",
                                    "type_time": mt5.ORDER_TIME_GTC,
                                    "type_filling": mt5.ORDER_FILLING_RETURN,
                                }
                    result_Pending_Sell = mt5.order_send(Request_Pending_Sell)

    def side(self):
        self.combobox_1 = self.combobox_1.get()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def Options(self):
        if self.radio_var.get()==2:
            print('Manual')
            self.entry.configure(state="normal")
            self.combobox_1.configure(state="normal")
        if self.radio_var.get()==1:
            print('Auto')
            self.entry.configure(state="disabled")
            self.combobox_1.configure(state="disabled")
            
    def Stop(self):
        exit()

    def Close_All_Positions(self):
        positions = mt5.positions_get()
        def close_position(position):
            tick = mt5.symbol_info_tick(position.symbol)
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,
                "deviation": 20,
                "magic": 100,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            return result
        for position in positions:
            close_position(position)

    def Close_Onepercent(self):
        positions = mt5.positions_get()
        def close_some(position):
            tick = mt5.symbol_info_tick(position.symbol)
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": 0.01,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,
                "deviation": 20,
                "magic": 100,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            return result
        for position in positions:
            close_some(position)

    def Close_Pend(self):
        positions = mt5.orders_get()
        def close_position(position):
            tick = mt5.symbol_info_tick(position.symbol)
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": position.ticket,
                "symbol": position.symbol,
                "type": mt5.ORDER_TYPE_BUY_STOP if position.type == 4 else mt5.ORDER_TYPE_SELL_STOP,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC
            }
            result = mt5.order_send(request)
            return result
        for position in positions:
            close_position(position)
        print('Pendings Removed')

    def Risk_Free(self):
                print('Risk Free On')
                MAX_DIST_SL = 0.0006
                TRAIL_AMOUNT = 0.0003
                DEFAULT_SL = 0.0003
                def trail_sl():
                    position = mt5.positions_get()
                    if mt5.positions_total()==0 or mt5.positions_total()==None:
                            #print('No Open Trade')
                            time.sleep(0.5)
                            trail_sl()
                    else:
                        #if mt5.positions_total()<=1:
                        i = mt5.positions_total()-1
                        position = position[i]
                        order_type = position.type
                        price_current = position.price_current
                        price_open = position.price_open
                        sl = position.sl
                        dist_from_sl = abs(round(price_current - sl, 6))
                        if dist_from_sl > MAX_DIST_SL:
                            if sl != 0.0:
                                if order_type == 0:
                                    new_sl = sl + TRAIL_AMOUNT
                                elif order_type == 1:
                                    new_sl = sl - TRAIL_AMOUNT
                            else:
                                new_sl = price_open - DEFAULT_SL if order_type == 0 else price_open + DEFAULT_SL
                            request = {
                                'action': mt5.TRADE_ACTION_SLTP,
                                'position': position.ticket,
                                'sl': new_sl,
                            }
                            result = mt5.order_send(request)
                            #print(result)
                            return result
                __name__ == '__main__'
                while True:
                        result = trail_sl()
                        time.sleep(0.5)


if __name__ == "__main__":
    app = App()
    app.mainloop()