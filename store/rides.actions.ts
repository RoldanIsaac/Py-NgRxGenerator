// ------------------------------------------------------------------------------------------
// @ Ride Actions
// ------------------------------------------------------------------------------------------

import { createAction, props } from "@ngrx/store";

// Load all Rides
export const loadRides = createAction("[Ride] Load Rides");
export const loadRidesSuccess = createAction(
  "[Ride] Load Rides Success",
  props<{ rides: any[] }>()
);
export const loadRidesFailure = createAction(
  "[Ride] Load Rides Failure",
  props<{ error: string }>()
);

// Load single Ride
export const loadRide = createAction(
  "[Ride] Load Ride",
  props<{ id: number }>()
);
export const loadRideSuccess = createAction(
  "[Ride] Load Ride Success",
  props<{ ride: any }>()
);
export const loadRideFailure = createAction(
  "[Ride] Load Ride Failure",
  props<{ error: string }>()
);

// Create
export const createRide = createAction(
  "[Ride] Create Ride",
  props<{ data: string }>()
);
export const createRideSuccess = createAction(
  "[Ride] Create Ride Success",
  props<{ ride: any; success: string }>()
);
export const createRideFailure = createAction(
  "[Ride] Create Ride Failure",
  props<{ error: string }>()
);

// Update
export const updateRide = createAction(
  "[Ride] Update Ride",
  props<{ data: string; id: number }>()
);
export const updateRideSuccess = createAction(
  "[Ride] Update Ride Success",
  props<{ ride: any; success: string }>()
);
export const updateRideFailure = createAction(
  "[Ride] Update Ride Failure",
  props<{ error: string }>()
);

// Delete
export const deleteRide = createAction(
  "[Ride] Delete Ride",
  props<{ id: number }>()
);
export const deleteRideSuccess = createAction(
  "[Ride] Delete Ride Success",
  props<{ id: number; success: string }>()
);
export const deleteRideFailure = createAction(
  "[Ride] Delete Ride Failure",
  props<{ error: string }>()
);
