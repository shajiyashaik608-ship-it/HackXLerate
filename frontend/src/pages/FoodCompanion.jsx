import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import MealCard from '../components/MealCard';
import MealFilters from '../features/nutrition/MealFilters';
import MealPlanner from '../features/nutrition/MealPlanner';
import MealDetails from '../features/nutrition/MealDetails';
import { SAMPLE_MEALS } from '../data/sampleMeals';

export default function FoodCompanion({
  dailyPlan,
  setDailyPlan,
  language
}) {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDiet, setSelectedDiet] = useState('all');
  const [budgetOnly, setBudgetOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeDetailMeal, setActiveDetailMeal] = useState(null);

  const isTelugu = language === 'te';

  const filteredMeals = SAMPLE_MEALS.filter((meal) => {
    const matchesCategory = selectedCategory === 'all' || meal.category === selectedCategory;
    const matchesDiet = selectedDiet === 'all' || meal.dietType === selectedDiet;
    const matchesBudget = !budgetOnly || meal.budgetIndicator === 'budget_friendly';
    const matchesSearch =
      meal.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      meal.ingredients.some((i) => i.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesCategory && matchesDiet && matchesBudget && matchesSearch;
  });

  const handleSelectMeal = (meal) => {
    const slot = meal.category === 'breakfast' ? 'breakfast' : meal.category === 'lunch' ? 'lunch' : 'dinner';
    setDailyPlan((prev) => ({
      ...prev,
      [slot]: prev[slot]?.id === meal.id ? null : meal
    }));
  };

  const handleRemoveMeal = (slot) => {
    setDailyPlan((prev) => ({ ...prev, [slot]: null }));
  };

  const handleResetPlan = () => {
    setDailyPlan({ breakfast: null, lunch: null, dinner: null });
  };

  return (
    <div>
      <PageHeader
        title={isTelugu ? 'భారతీయ ఆహార సహచరుడు (PCOS Nutrition)' : 'Indian Food PCOS Companion'}
        subtitle={isTelugu
          ? 'కఠినమైన డైటింగ్‌లు లేకుండా, మన నిత్య జీవితంలో లభించే పెసరట్టు, కొర్రలు, పప్పుల ద్వారా స్థిరమైన హార్మోన్ల సమతుల్యత.'
          : 'Sustainable, balanced nutrition using accessible Indian pantry staples. Focuses on steady glucose response and protein pairing without extreme restrictions.'}
      />

      {/* Daily Planner Widget */}
      <MealPlanner
        dailyPlan={dailyPlan}
        onRemoveMeal={handleRemoveMeal}
        onResetPlan={handleResetPlan}
      />

      {/* Filters Bar */}
      <MealFilters
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
        selectedDiet={selectedDiet}
        onSelectDiet={setSelectedDiet}
        budgetOnly={budgetOnly}
        onToggleBudget={setBudgetOnly}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />

      {/* Meals Grid */}
      <div className="grid-3">
        {filteredMeals.map((meal) => {
          const isSelected =
            dailyPlan.breakfast?.id === meal.id ||
            dailyPlan.lunch?.id === meal.id ||
            dailyPlan.dinner?.id === meal.id;

          return (
            <MealCard
              key={meal.id}
              meal={meal}
              isSelected={isSelected}
              onSelect={handleSelectMeal}
              onViewDetails={setActiveDetailMeal}
            />
          );
        })}
      </div>

      {/* Recipe Detail Modal */}
      <MealDetails
        meal={activeDetailMeal}
        isOpen={Boolean(activeDetailMeal)}
        onClose={() => setActiveDetailMeal(null)}
      />
    </div>
  );
}
