# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 08:44:17 2025

@author: manis
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PizzaDeliveryGame:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.facility_cost = 2000
        self.delivery_cost_per_mile = 1
        
        if 'facilities' not in st.session_state:
            st.session_state.facilities = []
        if 'demand_map' not in st.session_state:
            st.session_state.demand_map = np.random.randint(10, 50, (grid_size, grid_size))

    def add_facility(self, x, y):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            st.session_state.facilities.append((x, y))
            return True
        return False

    def calculate_costs(self):
        facility_costs = len(st.session_state.facilities) * self.facility_cost
        delivery_costs = 0
        
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if st.session_state.demand_map[x, y] > 0:
                    min_distance = float('inf')
                    for fx, fy in st.session_state.facilities:
                        distance = np.sqrt((x - fx)**2 + (y - fy)**2)
                        min_distance = min(min_distance, distance)
                    delivery_costs += min_distance * self.delivery_cost_per_mile * st.session_state.demand_map[x, y]
        
        return facility_costs, delivery_costs

    def plot_network(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(st.session_state.demand_map, cmap='YlOrRd', ax=ax)
        
        for fx, fy in st.session_state.facilities:
            ax.plot(fy + 0.5, fx + 0.5, 'b^', markersize=10)
        
        return fig

def main():
    st.title("🍕 Pizza Delivery Empire Game")
    st.write("Optimize your pizza delivery network!")
    
    game = PizzaDeliveryGame()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.pyplot(game.plot_network())
    
    with col2:
        st.subheader("Add New Facility")
        x = st.number_input("X coordinate", 0, 9, step=1)
        y = st.number_input("Y coordinate", 0, 9, step=1)
        
        if st.button("Add Facility"):
            if game.add_facility(x, y):
                st.success(f"Facility added at ({x}, {y})!")
            else:
                st.error("Invalid location!")
    
    if st.button("Calculate Costs"):
        facility_costs, delivery_costs = game.calculate_costs()
        total_costs = facility_costs + delivery_costs
        
        st.subheader("📊 Cost Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Facility Costs", f"${facility_costs:,.2f}")
        col2.metric("Delivery Costs", f"${delivery_costs:,.2f}")
        col3.metric("Total Costs", f"${total_costs:,.2f}")
    
    if st.button("Reset Game"):
        st.session_state.facilities = []
        st.session_state.demand_map = np.random.randint(10, 50, (game.grid_size, game.grid_size))
        st.experimental_rerun()

if __name__ == "__main__":
    main()