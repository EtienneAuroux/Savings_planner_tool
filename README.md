# Savings_planner_tool
## A web app to plan your savings and investments in a realistic way.

#### Direct link to the app:

[https://savings-planner-app.herokuapp.com](https://savings-planner-app.herokuapp.com)

#### Why this app?

Since the apparition of low-cost brokers (Robinhood, Nordnet, ...) more and more people are investing their savings with the hope of growing their wealth. Although many forms of investment exist (savings accounts, real estate, government bills, corporate bond, commodities, ...), the lure of a quick buck pushes most non-professional investors to buy and sell only common stocks, often over very short periods of time. What they see are the few lucky (and skilled?) investors who become wealthy enough to write books and have successful investing YouTube channels. However, for each of these _investing gurus_ how many others lose part or all of their hard-earned money?

Losing one's savings can have devastating consequences for one's mental well-being and financial future. In most cases, it is not a sign of lacking intelligence but rather of lacking exposure to diverse forms of financial education. If all you hear is tales of people buying 1000$ worth of stocks and becoming millionaires the next week, how can it not seem easy?

This **Savings planner tool** was made with the opposite mindset. It assumes that, like me, you hate risk, you have no particular desire to reach obscene levels of wealth and your only concern is financial safety. That being said, this tool is for informational purposes only and does not constitue financial advice in any shape or form. Should you choose to invest your money, you will do so at your own peril; any kind of investment has risks that come with it and it will never be possible to guarantee complete financial safety. I am not a financial advisor and you should always do your own research on an investment before spending your money. I strongly recommend that you consult a professional investment advisor before making any investment decisions!


#### What does this app do?

- It calculates the minimum amount of money you will have to contribute to your portfolio each year in order to be able to reach your saving goal.
- It takes into account five forms of investment: 
    - Traditional bank accounts. This is where we have our everyday money, for most of us it might be the only place where we stock our money.
    - Government bills. This is how your government borrow money, by selling you securities and paying you back in a given number of years with interests. Typically the return on investment is low (a few percents) but it is perhaps the safest method of investment. You can only lose your money if your government falls.
    - Corporate bonds. This is the same as government bills but for companies' debts. It's a way for companies to borrow money with the promise to reimburse you after some time with interests.
    - Real estate. This is the buying and selling of houses, appartments, buildings or pieces of lands.
    - Common stocks. Stocks are pieces of a company, when you buy a stock you partially own the company.
- It quantifies the risk involved with an investment from _very low_ risk (government bills for examples) to _very high_ risk (common stocks for example).
- It allows the user to personalize the portfolio in terms of risks or in terms of allocation and rates of return.
- It takes into account the country in which the user wants to invest.

#### What doesn't this app do?

- It does not recommend any particular investment. For example, it will never tell you "buy the stock of company A".
- It does not take into account investing in different countries other than the one selected.
- It does not take into account inflation.
- It does not work for investing periods smaller than a year.
- It does not foresee the future in any way, shape or form.

#### Is this app perfect?

Absolutely not! So many things could be improved I am sure but it represents what I can do with my current skills. Here is a list of what could be improved (that I am aware of):
- In app.py and support_functions.py:
    - Improve the algorithm for the calculation of the minimum yearly contribution.
    - Find a way to fixate the dimensions of the plotly graphs so that it remains unchanged when zoomed in/out.
- In assets\1_layout.css:
    - Find a way to position all the scalable element nicely without relying on position:absolute.
    - Implement more unifying classes instead of having almost one class per element.
- In general:
    - Add more countries.
    - Make it more user friendly, right now it is a bit unclear how to use the app if you've never used it before.
