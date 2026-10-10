from typing import List, Dict, Any, Optional

INDIAN_PCOS_MEAL_DATABASE = [
    {
        "dish_name": "Moong Dal Pesarattu with Ginger Chutney",
        "meal_type": "breakfast",
        "diet_type": "vegetarian",
        "ingredients": ["Whole green moong dal", "Ginger", "Green chillies", "Cumin", "Onions"],
        "why_it_works_for_pcos": "Whole moong dal has a low glycemic index and provides 14g of plant protein, preventing morning insulin spikes.",
        "protein_grams": 14,
        "fibre_grams": 9,
        "glycemic_index": "low",
        "budget_friendly": True
    },
    {
        "dish_name": "Sprouted Methi & Kala Chana Chaat",
        "meal_type": "snack",
        "diet_type": "vegetarian",
        "ingredients": ["Sprouted black chana", "Fenugreek sprouts", "Cucumber", "Lemon juice", "Chaat masala"],
        "why_it_works_for_pcos": "Fenugreek (methi) contains 4-hydroxyisoleucine which supports healthy glucose tolerance; high in dietary soluble fibre.",
        "protein_grams": 10,
        "fibre_grams": 8,
        "glycemic_index": "low",
        "budget_friendly": True
    },
    {
        "dish_name": "Foxtail Millet (Korralu) with Palak Dal & Curd",
        "meal_type": "lunch",
        "diet_type": "vegetarian",
        "ingredients": ["Foxtail millet", "Spinach (Palak)", "Toor dal", "Fresh probiotic curd"],
        "why_it_works_for_pcos": "Swapping white polished rice with foxtail millet slows glucose release. Spinach supplies magnesium which assists hormone regulation.",
        "protein_grams": 16,
        "fibre_grams": 11,
        "glycemic_index": "medium",
        "budget_friendly": True
    },
    {
        "dish_name": "Grilled Paneer & Veggie Skewers with Mint Raita",
        "meal_type": "dinner",
        "diet_type": "vegetarian",
        "ingredients": ["Low-fat paneer", "Capsicum", "Onion", "Tomato", "Curd mint dip"],
        "why_it_works_for_pcos": "High-protein, minimal-carb evening meal supporting steady overnight blood glucose levels.",
        "protein_grams": 18,
        "fibre_grams": 4,
        "glycemic_index": "low",
        "budget_friendly": False
    },
    {
        "dish_name": "Boiled Egg Podi Curry with 2 Multigrain Rotis",
        "meal_type": "dinner",
        "diet_type": "eggitarian",
        "ingredients": ["Eggs (2)", "Kandi podi/curry leaves powder", "Whole wheat & jowar roti"],
        "why_it_works_for_pcos": "Choline from whole eggs supports liver metabolism and hormonal clearance; complex grain rotis promote satiety.",
        "protein_grams": 19,
        "fibre_grams": 6,
        "glycemic_index": "low",
        "budget_friendly": True
    },
    {
        "dish_name": "Chepala Pulusu (South Indian Fish Curry) with Brown Rice",
        "meal_type": "lunch",
        "diet_type": "non_vegetarian",
        "ingredients": ["Rohu/Salmon fish", "Tamarind", "Fenugreek seeds", "Brown rice / Quinoa"],
        "why_it_works_for_pcos": "Fish provides anti-inflammatory Omega-3 fatty acids, which help mitigate chronic low-grade inflammation commonly observed in PCOS.",
        "protein_grams": 24,
        "fibre_grams": 4,
        "glycemic_index": "low",
        "budget_friendly": False
    }
]

class FoodRecommender:
    """
    Indian Nutrition Recommender for PCOS lifestyle support.
    Focuses on affordable pantry staples, low GI carbs, and high protein.
    """
    
    @staticmethod
    def get_recommendations(
        diet_type: str = "vegetarian",
        meal_type: Optional[str] = None,
        budget_friendly_only: bool = False
    ) -> List[Dict[str, Any]]:
        results = []
        for meal in INDIAN_PCOS_MEAL_DATABASE:
            # Filter by diet type (vegetarian can eat vegetarian; eggitarian can eat veg + egg; non-veg can eat all)
            if diet_type == "vegetarian" and meal["diet_type"] != "vegetarian":
                continue
            if diet_type == "eggitarian" and meal["diet_type"] not in ["vegetarian", "eggitarian"]:
                continue
                
            # Filter by meal type
            if meal_type and meal["meal_type"] != meal_type:
                continue
                
            # Filter by budget
            if budget_friendly_only and not meal["budget_friendly"]:
                continue
                
            results.append(meal)
            
        if not results:
            # Fallback to general vegetarian options if filters were too restrictive
            return [m for m in INDIAN_PCOS_MEAL_DATABASE if m["diet_type"] == "vegetarian"]
            
        return results

    @staticmethod
    def get_lifestyle_guidance() -> str:
        return (
            "Key Indian Nutrition Principles for PCOS:\n"
            "1. Pair carbohydrates (rice/roti/idli) with adequate protein (dal, sprouts, paneer, eggs).\n"
            "2. Incorporate traditional seeds: Methi (fenugreek) and flaxseeds support insulin sensitivity.\n"
            "3. Aim for sustainable eating rather than extreme elimination diets."
        )
