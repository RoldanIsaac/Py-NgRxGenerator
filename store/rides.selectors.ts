import { createFeatureSelector, createSelector } from "@ngrx/store";
import { RideState, RidesState } from "./rides.reducer";

// -----------------------------------------------------------------------------------------------------
// @ Feature Selectors
// -----------------------------------------------------------------------------------------------------

export const selectRidesState = createFeatureSelector<RidesState>("rides");

// -----------------------------------------------------------------------------------------------------
// @ Ride
// -----------------------------------------------------------------------------------------------------

export const selectAllRides = createSelector(
  selectRidesState,
  (state: RidesState) => state.rides
);

export const selectSingleRide = createSelector(
  selectRidesState,
  (state: RidesState) => state.ride
);
