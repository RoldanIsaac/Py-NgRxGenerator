import { createFeatureSelector, createSelector } from '@ngrx/store';
import { RideState, RidesState } from './rides.reducer';

// -----------------------------------------------------------------------------------------------------
// @ Feature Selectors
// -----------------------------------------------------------------------------------------------------

export const selectAllRidesState = createFeatureSelector<RidesState>('rides');

export const selectSingleRideState = createFeatureSelector<RideState>('ride');

// -----------------------------------------------------------------------------------------------------
// @ Ride
// -----------------------------------------------------------------------------------------------------

export const selectAllRides = createSelector(
    selectAllRidesState,
    (state: RidesState) => state.rides
);

export const selectSingleRide = createSelector(
    selectSingleRideState,
    (state: RideState) => state.ride
);
