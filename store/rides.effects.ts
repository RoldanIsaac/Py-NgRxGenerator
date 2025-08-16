import { inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { AlertService } from 'app/services/alert.service';
import { LoggerService } from 'app/services/logger.service';
import { catchError, map, of, switchMap, tap } from 'rxjs';

import { RidesService } from '../services/rides.service';
import * as RideActions from './rides.actions';

@Injectable()
export class RidesEffects {
    private _actions$ = inject(Actions);
    private _store = inject(Store);
    private _logger = inject(LoggerService);
    private _rideService = inject(RidesService);
    private _alertService = inject(AlertService);

    messages = {
        getAllError: 'Error getting all rides',
        connectionError: 'Error connecting to the server',
        unknownError: 'Unknown error',
    };

    // ------------------------------------------------------------------------------------------
    // @ Effects
    // ------------------------------------------------------------------------------------------

    // Get All Rides
    getAllRides$ = createEffect(() =>
        this._actions$.pipe(
            ofType(RideActions.loadRides),
            switchMap(() => {
                return this._rideService.getAll().pipe(
                    map((res) => {
                        return RideActions.loadRidesSuccess({
                            rides: res.data,
                        });
                    }),
                    catchError((error) =>
                        of(
                            RideActions.loadRidesFailure({
                                error:
                                    error?.error?.message ||
                                    this.messages.unknownError,
                            })
                        )
                    )
                );
            })
        )
    );

    // Get One Ride
    getRide$ = createEffect(() =>
        this._actions$.pipe(
            ofType(RideActions.loadRide),
            switchMap((action) => {
                return this._rideService.getOne(action.id).pipe(
                    map((res) => {
                        return RideActions.loadRideSuccess({
                            ride: res.data,
                        });
                    }),
                    catchError((error) =>
                        of(
                            RideActions.loadRideFailure({
                                error:
                                    error?.error?.message ||
                                    this.messages.unknownError,
                            })
                        )
                    )
                );
            })
        )
    );

    // Create Ride
    createRide$ = createEffect(() =>
        this._actions$.pipe(
            ofType(RideActions.createRide),
            switchMap((action) => {
                return this._rideService.create(action.rideData).pipe(
                    map((res) => {
                        return RideActions.createRideSuccess({
                            ride: res.data,
                            success: 'Ride created successfully',
                        });
                    }),
                    catchError((error) =>
                        of(
                            RideActions.createRideFailure({
                                error:
                                    error?.error?.message ||
                                    this.messages.unknownError,
                            })
                        )
                    )
                );
            })
        )
    );

    // Update Ride
    updateRide$ = createEffect(() =>
        this._actions$.pipe(
            ofType(RideActions.updateRide),
            switchMap((action) => {
                return this._rideService
                    .update(action.rideData, action.id)
                    .pipe(
                        map((res) => {
                            return RideActions.updateRideSuccess({
                                ride: res.data,
                                success: 'Ride updated successfully',
                            });
                        }),
                        catchError((error) =>
                            of(
                                RideActions.updateRideFailure({
                                    error:
                                        error?.error?.message ||
                                        this.messages.unknownError,
                                })
                            )
                        )
                    );
            })
        )
    );

    // Delete Ride
    deleteRide$ = createEffect(() =>
        this._actions$.pipe(
            ofType(RideActions.deleteRide),
            switchMap((action) => {
                return this._rideService.delete(action.id).pipe(
                    map(() => {
                        return RideActions.deleteRideSuccess({
                            id: action.id,
                            success: 'Ride deleted successfully',
                        });
                    }),
                    catchError((error) =>
                        of(
                            RideActions.deleteRideFailure({
                                error:
                                    error?.error?.message ||
                                    this.messages.unknownError,
                            })
                        )
                    )
                );
            })
        )
    );

    // ------------------------------------------------------------------------------------------
    // @ Alerts
    // ------------------------------------------------------------------------------------------

    onRideActionSuccess$ = createEffect(
        () =>
            this._actions$.pipe(
                ofType(
                    RideActions.createRideSuccess,
                    RideActions.updateRideSuccess,
                    RideActions.deleteRideSuccess
                ),
                tap((action) => {
                    this._alertService.showAlert(action.success, 'success');
                })
            ),
        { dispatch: false }
    );

    onRideActionFailure$ = createEffect(
        () =>
            this._actions$.pipe(
                ofType(
                    RideActions.loadRidesFailure,
                    RideActions.loadRideFailure,
                    RideActions.createRideFailure,
                    RideActions.updateRideFailure,
                    RideActions.deleteRideFailure
                ),
                tap((action) => {
                    this._alertService.showAlert(action.error, 'error');
                })
            ),
        { dispatch: false }
    );
}
