from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(model_name="sentence-transformers/all-MiniLM-L6-v2")

faq = Route(
    name="faq",
    utterances=[
        "What is the return policy?",
        "How do I return a product?",
        "Can I return an item?",
        "How long does a refund take?",
        "When will I get my refund?",
        "How can I track my order?",
        "Where is my order?",
        "Can I cancel my order?",
        "Can I modify my order?",
        "Can I change my order after placing it?",
        "What payment methods are accepted?",
        "Can I pay by credit card?",
        "How long does an order take to process?",
        "When will my order be shipped?",
        "How does shipping work?",
        "What should I do if my order has not arrived?"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "Show me Nike shoes.",
        "Find Nike shoes.",
        "I want Nike shoes.",
        "Show me Nike products.",
        "Find shoes under Rs 300.",
        "Show me products below Rs 500.",
        "Which products are under Rs 1000?",
        "Show me the cheapest shoes.",
        "Show me the most expensive shoes.",
        "Show me the top rated products.",
        "Which shoes have the highest rating?",
        "Find products with rating above 4.5.",
        "Show me products with a discount.",
        "Which Nike products have a discount?",
        "Find Nike shoes with more than 20 percent discount.",
        "Show me Puma running shoes.",
        "What is the price of Nike shoes?",
        "How much do Puma running shoes cost?",
        "Show me the best Nike shoes.",
        "Find the top 3 Nike shoes.",
        "Show me the top 3 Nike shoes under Rs 300.",
        "Find the best shoes below Rs 1000.",
        "Which Nike shoes are under Rs 500?",
        "Show me Adidas shoes below Rs 2000.",
        "Find shoes between Rs 500 and Rs 1500.",
        "Show products with a rating above 4.8.",
        "Find Nike shoes under Rs 1000 with a discount."
    ]
)

small_talk = Route(
    name="small_talk",
    utterances=[
        "Hello",
        "Hi",
        "Hey",
        "How are you?",
        "What's up?",
        "Good morning",
        "Good afternoon",
        "Good evening",
        "How's it going?",
        "Nice to meet you",
        "How can I help you?",
        "What can I do for you?",
        "Can you help me?",
        "I need assistance",
        "I have a question",
        "Can you answer my question?",
        "I have a problem",
        "Can you solve my problem?",
        "I need support",
        "Can you provide support?"
    ]
)

router = SemanticRouter(routes=[faq, sql, small_talk], encoder=encoder, auto_sync="local")

# router.set_threshold(0.3)
router.set_threshold(0.2, route_name="faq")
router.set_threshold(0.35, route_name="sql")
router.set_threshold(0.4, route_name="small_talk")

if __name__ == "__main__":
    print(router.get_thresholds())
    print(router("Can I cancel or modify my order after placing it?").name)
    print(router("What is the price of adidas running shoes with discount?").name)