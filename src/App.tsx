import React, { useState } from 'react';
import { SignupForm } from './components/SignupForm';
import { CategorySelection } from './components/CategorySelection';
import { NewsFeed } from './components/NewsFeed';
import { User, Category } from './types';

type AppStep = 'signup' | 'categories' | 'feed';

function App() {
  const [currentStep, setCurrentStep] = useState<AppStep>('signup');
  const [user, setUser] = useState<User | null>(null);

  const handleSignup = (name: string, email: string) => {
    setUser({
      name,
      email,
      selectedCategories: []
    });
    setCurrentStep('categories');
  };

  const handleCategorySelection = (categories: Category[]) => {
    if (!user) return;

    const updatedUser = {
      ...user,
      selectedCategories: categories
    };

    setUser(updatedUser);
    setCurrentStep('feed');
  };

  const handleBackToCategories = () => {
    setCurrentStep('categories');
  };

  return (
    <div className="App">
      {currentStep === 'signup' && (
        <SignupForm onSubmit={handleSignup} />
      )}
      
      {currentStep === 'categories' && user && (
        <CategorySelection
          userName={user.name}
          onSubmit={handleCategorySelection}
        />
      )}
      
      {currentStep === 'feed' && user && (
        <NewsFeed
          user={user}
          onBack={handleBackToCategories}
        />
      )}
    </div>
  );
}

export default App;