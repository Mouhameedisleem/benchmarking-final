import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000 < Date.now();
  } catch {
    return true;
  }
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');

  // Never block or redirect for auth endpoints (login, register, etc.)
  const isAuthEndpoint = req.url.includes('/api/auth/');

  if (!isAuthEndpoint && token && isTokenExpired(token)) {
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    router.navigate(['/login']);
    return throwError(() => new HttpErrorResponse({ status: 401, statusText: 'Token expired' }));
  }

  // Don't attach an expired token to any request
  const validToken = token && !isTokenExpired(token) ? token : null;
  const authReq = validToken
    ? req.clone({ setHeaders: { Authorization: `Bearer ${validToken}` } })
    : req;

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && !isAuthEndpoint) {
        localStorage.removeItem('token');
        localStorage.removeItem('currentUser');
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};
