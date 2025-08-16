import { createReducer, on } from '@ngrx/store';
import * as RideActions from './rides.actions';
import { Ride } from './rides.models';

// -----------------------------------------------------------------------------------------------------
// @ States
// -----------------------------------------------------------------------------------------------------

export interface RidesState {
    rides: Ride[];
    isLoading: boolean;
    error: string | null;
}

export interface RideState {
    ride: Ride;
    isLoading: boolean;
    error: string | null;
}

// -----------------------------------------------------------------------------------------------------
// @ Initial States
// -----------------------------------------------------------------------------------------------------

export const initialRidesState: RidesState = {
    rides: [],
    isLoading: false,
    error: null,
};

export const initialRideState: RideState = {
    ride: null,
    isLoading: false,
    error: null,
};

// -----------------------------------------------------------------------------------------------------
// @ Reducers
// -----------------------------------------------------------------------------------------------------

// All Rides Reducer
export const ridesReducer = createReducer(
    initialRidesState,

    // On Load Rides
    on(RideActions.loadRides, (state) => ({
        ...state,
        isLoading: true,
    })),
    on(RideActions.loadRidesSuccess, (state, { rides }) => ({
        ...state,
        isLoading: false,
        rides: rides,
    })),
    on(RideActions.loadRidesFailure, (state, { error }) => ({
        ...state,
        isLoading: false,
        error: error,
    })),

    // On Create
    on(RideActions.createRide, (state) => ({
        ...state,
        isLoading: true,
    })),
    on(RideActions.createRideSuccess, (state, { ride }) => ({
        ...state,
        isLoading: false,
        rides: [...state.rides, ride],
    })),
    on(RideActions.createRideFailure, (state, { error }) => ({
        ...state,
        isLoading: false,
        error: error,
    })),

    // On Update
    on(RideActions.updateRide, (state) => ({
        ...state,
        isLoading: true,
    })),
    on(RideActions.updateRideSuccess, (state, { ride }) => ({
        ...state,
        isLoading: false,
        rides: state.rides.map((r) => (r.id === ride.id ? ride : r)),
    })),
    on(RideActions.updateRideFailure, (state, { error }) => ({
        ...state,
        isLoading: false,
        error: error,
    })),

    // On Delete
    on(RideActions.deleteRide, (state) => ({
        ...state,
        isLoading: true,
    })),
    on(RideActions.deleteRideSuccess, (state, { id }) => ({
        ...state,
        isLoading: false,
        rides: state.rides.filter((r) => r.id !== id),
    })),
    on(RideActions.deleteRideFailure, (state, { error }) => ({
        ...state,
        isLoading: false,
        error: error,
    }))
);

// Single Ride Reducer
export const rideReducer = createReducer(
    initialRideState,

    // On Load Single Ride
    on(RideActions.loadRide, (state) => ({
        ...state,
        isLoading: true,
    })),
    on(RideActions.loadRideSuccess, (state, { ride }) => ({
        ...state,
        isLoading: false,
        ride: ride,
    })),
    on(RideActions.loadRideFailure, (state, { error }) => ({
        ...state,
        isLoading: false,
        error: error,
    }))
);
