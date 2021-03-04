from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import FloatField, Count, Avg, Sum, F

from .serializers import TradeSerializer, PortfolioSerializer
from .models import Trade, Portfolio
# Create your views here.

#for route /trades
class TradeList(APIView):

    def get(self, request, format=None):
        trades = Trade.objects.all()
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TradeSerializer(data=request.data)

        #check whether the selling quantity is more than the buy quantity or not
        #if it is more than the buy quantity, don't accept the trade
        if request.data['trade_type'] == "SELL":
            total_buy_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'), total_price = Sum(F('price')* F('quantity'), output_field=FloatField())).filter(trade_type="BUY", ticker=request.data['ticker'])
            total_sell_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'), total_price = Sum(F('price')* F('quantity'), output_field=FloatField())).filter(trade_type="SELL", ticker=request.data['ticker'])
            print(total_sell_trades)
            print(total_buy_trades)

            new_trade_quantity = request.data['quantity']

            if len(total_sell_trades) == 0:
                total_sell_quantity = 0
            else:
                total_sell_quantity = total_sell_trades[0]['total_quantity']

            if len(total_buy_trades) == 0:
                total_buy_quantity = 0
            else:
                total_buy_quantity = total_buy_trades[0]['total_quantity']

            total_available_quantity = total_buy_quantity - total_sell_quantity

            # if quantity of shares change to negative, decline the creation of new trade
            if (total_available_quantity - new_trade_quantity) < 0:
                return Response({"detail": "method not allowed quantity can not be negative"})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete all the trades
    def delete(self, request, format=None):
        trades = Trade.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#for route /trades/<pk>
class TradeDetail(APIView):

    def get_object(self, pk):
        try:
            return Trade.objects.get(pk=pk)
        except Trade.DoesNotExist:
            raise Http404
    
    # get a specific trade
    def get(self, request, pk, format=None):
        trade = self.get_object(pk)
        serializer = TradeSerializer(trade)
        return Response(serializer.data)

    # update a previous trade
    #in such a way that quantity doesn't go negative
    def put(self, request, pk, format=None):
        trade = self.get_object(pk)
        serializer = TradeSerializer(trade, data=request.data)

        # check whether the updated quantity becomes negative or not
        total_buy_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'), total_price = Sum(F('price')* F('quantity'), output_field=FloatField())).filter(trade_type="BUY", ticker=request.data['ticker'])
        total_sell_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'), total_price = Sum(F('price')* F('quantity'), output_field=FloatField())).filter(trade_type="SELL", ticker=request.data['ticker'])

        old_trade_quantity = trade.quantity
        new_trade_quantity = request.data['quantity']

        if len(total_sell_trades) == 0:
            total_sell_quantity = 0
        else:
            total_sell_quantity = total_sell_trades[0]['total_quantity']

        if len(total_buy_trades) == 0:
            total_buy_quantity = 0
        else:
            total_buy_quantity = total_buy_trades[0]['total_quantity']

        total_available_quantity = total_buy_quantity - total_sell_quantity

        if (request.data['trade_type'] == "SELL"):
            new_trade_quantity = -new_trade_quantity

        # if quantity of shares change to negative, decline the update
        if (total_available_quantity - old_trade_quantity + new_trade_quantity) < 0:
            return Response({"detail": "method not allowed, quantity can not be negative"})

        # if the quantity is positive and data is valid, then update the trade
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        trade = self.get_object(pk)

        total_buy_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'), total_price = Sum(F('price')* F('quantity'), output_field=FloatField())).filter(trade_type="BUY", ticker=request.data['ticker'])
        total_sell_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'), total_price = Sum(F('price')* F('quantity'), output_field=FloatField())).filter(trade_type="SELL", ticker=request.data['ticker'])

        old_trade_quantity = trade.quantity

        if len(total_sell_trades) == 0:
            total_sell_quantity = 0
        else:
            total_sell_quantity = total_sell_trades[0]['total_quantity']

        if len(total_buy_trades) == 0:
            total_buy_quantity = 0
        else:
            total_buy_quantity = total_buy_trades[0]['total_quantity']

        total_available_quantity = total_buy_quantity - total_sell_quantity

        if (trade.trade_type == "BUY"):
            old_trade_quantity = -old_trade_quantity

        # if quantity of shares change to negative, decline the deletion
        if (total_available_quantity + old_trade_quantity) < 0:
            return Response({"detail": "method not allowed, quantity can not be negative"})

        # if the quantity is positive and data is valid, then delete the trade
        trade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PortfolioView(APIView):
    def get(self, request, format=None):

        #fetch the buy trades grouped by company
        buy_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'),
        total_price = Sum(F('price')* F('quantity'),
        output_field=FloatField())).filter(trade_type= "BUY")

        #iterate each buy trade for company and create a portfolio, or update an existing portfolio
        # for the company with updated quantity and average price
        for buy_trade in buy_trades:
            obj, created = Portfolio.objects.update_or_create(ticker=buy_trade['ticker'], defaults={'quantity':buy_trade['total_quantity'], 'average_buy_price':(buy_trade['total_price'] / buy_trade['total_quantity'])})
            # p.save()
        
        #fetch the sell trades grouped by company
        sell_trades = Trade.objects.values('ticker', 'trade_type').annotate(total_quantity = Sum('quantity'),
        total_price = Sum(F('price')* F('quantity'),
        output_field=FloatField())).filter(trade_type= "SELL")


        # decrement the quantity of shares by subtracting sell trades quantity
        # from the portfolio quantity
        for sell_trade in sell_trades:
            s = Portfolio.objects.get(ticker=sell_trade['ticker'])
            # s.save()
            s.quantity = s.quantity - sell_trade['total_quantity']
            s.save()


        #return the portfolio response
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        print(serializer.data)
        return Response(serializer.data)

        # return Response(status=status.HTTP_200_OK)

class ReturnsView(APIView):
    def get(self, request, format=None):

        #calculates the returns
        current_price = 100
        returns = Portfolio.objects.aggregate(returns = Sum( (current_price - F('average_buy_price')) * F('quantity'),output_field=FloatField()))
        return Response(returns)

