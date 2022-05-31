# new-listing. 

function:  
1. POST what you want to sell: input the name, category, price, discount(percent off) and image of the item.  
The image may be in any size, but it will be resized to a square afterwards.  

2. GET all items from the database: you may also group them by discount(must buy list) or category.  
(But if the item name overlaps with the category, the search will return that item twice, so the improvement may be unique the return items).  

3. GET items you're interested in by searching for the similar item categories or discount items.  
The discount items will be descending arangement according to their discount ratio, but because of the array filter shallow copy problem, after clicking to the "discount" grouping, the item list will only have discount item, so we need to click "id" grouping to fetch whole data from database.  
The useRef extended function of "autojump" to the next input block will only be at the third block in this demo.  

The UI design and the forward function is in figma : https://www.figma.com/file/0dPk1c4rvySvH4ZCQCjBbF/Must-have-List---Zhiyan?node-id=0%3A1
