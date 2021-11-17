# Retail KPIs
Retail KPIs is an app designed for retailers to analyse customer data and calculate store key performance indicators (KPIs). The user is able to update a spreadheet with sales figures, obtain automated figures for KPIs and get a predicted sales target for the next day, based on data collected from previous selling days. This allows the user to automatically update a spreadsheet with data, and obtain KPI results for easy analysis of store performance and customer purchase data.

<img src="assets/images/responsivity.png" alt="Image of Retail KPIs app on different screen sizes">

## Application Structure

The image below shows the application structure. This represents how the user will use the app, and the processes they will go through.
The red square always represents a menu, where the user is able to choose what to do from a menu of options. The blue curved shapes show the functions that are being used within the app. Here there are several different functions that are used within the app. Somtimes the same function is used more than once and the order that it is used is shown on the arrows attached to the function. The yellow vertical squares show where the user is required to input a value to be added to the spreadsheet. Green hexagons show where the user is able to view some data. There is a two way arrow attached to these shapes showing that they are able to go back to the menu of options after viewing this. 
Red circles represent where the user has chosen to exit the app. Lines with arrows show that the preceding step is necessary for the current step, where as line with no arrow heads just imply that that is the next step or order of step in the application.

<img src="assets/images/structure.png" alt="Flowchart showing the application structure">

## Database Structure

The structure of the database is shown below. There are three worksheets: sales figures, KPIs and sum sales target. The first worksheet, sales figures, is a worksheet of data that is collected by the user and then submitted to this app. The second worksheet, KPIs, shows the analysis of this data, which is calculated and added to the worksheet by functions, after the sales figures worksheet is updated. Finally, sum sales target is then calculated and updated, showing the sum sales target for the next day. Hence why there is 1 more row for sum sales target than there is for the others. As each row represents a day of business.

### Sales Figures

|Footfall|Sum sales £|Num sales|num items sold|
|---|---|---|---|
|300|40000|80|240|
|340|53000|124|266|
|320|45000|80|240|
|353|52000|75|233|

Footfall is a measure of the number of customers (AKA potential customers) that enter the store. This is usually measure by a doorman, or a device that is able to count as a person enters a store, for example. Sum sales is the revenue that the business makes. So, the total income before any outgoings. Num sales is the number of sales that are made. Num items sold is the total number of items that the business sells for that day.

### KPIs

|Conversion %|IPC|APC £|Sales EXP %|
|---|---|---|---|
|22|2|500|-19|
|24|2|529|-3|
|24|2|515|-15|
|25|3|530|-4.2|
|27|3|529|-3.5|

KPIs are then calculated from the sales figures that are submitted by the user. Conversion is a measure of the number of customers that buy something compared to the number of customers that enter the store. This value is usually measured as a percentage. IPC is the Items per customer, which represents the number of items bought on average per customer. APC is the average sale per customer. This is a measure of the everage transaction value. Sales EXP (or expectation) is a way to compare how far the actual sum sales is from the target. This is also measured as a percentage. If the sum sales is greater than the Next Trg, sales EXP will be positive. And if sum sales is less than Next Trg, sales EXP will be a negative.

### Sum Sales Target

|Next Trg £|
|---|
|42000|
|44000|
|45000|
|46500|
|47200|
|47600|

Sum sales Target or Next Trg is a prediction of the following day of sum sales made by the business. This value is measured by taking an average of the previous 5 days of business. If sum sales begin to increase, the target will be higher, and vice versa if sum sales decrease.

