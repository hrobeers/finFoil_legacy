subroutine naca4 ( x, thickness, y )
!*****************************************************************************80
!
!! NACA4 evaluates the naca 4-digit profile in one point.
!
!  Discussion:
!
!    Naca 4-digit profile
!
!  Licensing:
!
!    This code is distributed under the GNU LGPL license.
!
!  Modified:
!
!   21 May 2011
!
!  Author:
!
!    Hans Robeers
!
!  Parameters:
!
!    Input, real ( kind = 8 ) x, the relative abscissa value at which the spline
!    is to be evaluated. Normally, 0 <= x <= 1, and
!    the data will be interpolated.  For x outside this range,
!    extrapolation will be used.
!
!    Input, real ( kind = 8 ) thickness, the thickness of the naca profile.
!
!    Output, real ( kind = 8 ) y, the value of the spline at x.
!

!
! arguments
!
!   integer(kind=4), intent(in):: 
  real(kind=8), intent(in):: x, thickness
  real(kind=8), intent(out):: y

! local variables
!
  real(kind=8):: a1, b1, c1, d1, e1
!   integer(kind=4):: 
    
    a1 = 0.2969d0  * sqrt(x)
    b1 = -0.1260d0 * (x)
    c1 = -0.3516d0 * (x)**2
    d1 = 0.2843d0 * (x)**3
    e1 = -0.1015d0 * (x)**4
    y = thickness/0.2 * (a1+b1+c1+d1+e1) ! * chordlength

end

subroutine naca_val ( thickness, nval, yval )
!*****************************************************************************80
!
!! NACA_VAL evaluates a speciefied naca profile in a range of values.
!
!  Discussion:
!
!    The other subroutines only evaluate in one point, this
!    one wraps around them in FORTRAN for speed.
!
!  Licensing:
!
!    This code is distributed under the GNU LGPL license.
!
!  Modified:
!
!   21 May 2011
!
!  Author:
!
!    Hans Robeers
!
!  Parameters:
!
!    Input, real ( kind = 8 ) xval(nval), the relative abscissa value at which the spline
!    is to be evaluated. Normally, 0 <= x <= 1, and
!    the data will be interpolated.  For x outside this range,
!    extrapolation will be used.
!
!    Input, real ( kind = 8 ) thickness, the thickness of the naca profile.
!
!    Output, real ( kind = 8 ) y(nval), the value of the spline at x.
!

!
! arguments
!
  integer(kind=4), intent(in):: nval
  real(kind=8), intent(in):: thickness
  real(kind=8), intent(out):: yval(nval)

! local variables
!
  real(kind=8):: d, xval
!   integer(kind=4):: 
  
  d = 1d0/(nval-1)
  do i = 1, nval
    xval = (i-1)*d
    call naca4(xval, thickness, yval(i)) ! dim_num, ndata, tdata, ydata, tval, yval
  end do

end

subroutine make_surface( x_res, y_res, lead_grid, trail_grid, thickness, surf )
!
! arguments
!
  integer(kind=4), intent(in):: x_res, y_res, lead_grid(y_res), trail_grid(y_res)
  real(kind=8), intent(in):: thickness(y_res)
  real(kind=8), intent(out):: surf(x_res,y_res)

! local variables
!
  real(kind=8):: d, xval, yval, notanum
  integer(kind=4):: points
  real(kind=8):: arg = -1.0

  notanum = sqrt(arg)
  
  do i = 1, y_res
    points = trail_grid(i) - lead_grid(i)
!     surf[leading_edge_grid[i]:trailing_edge_grid[i],i] = naca_val(thick[i],points[i])
!     call naca_val(thickness(i),points,surf(leading_edge_grid(i):trailing_edge_grid(i),i))

    d = 1d0/(points-1)
    do j = 0, x_res-1
      if (j>=lead_grid(i) .and. j< trail_grid(i)) then
        xval = (j-lead_grid(i))*d
        call naca4(xval, thickness(i), yval) ! dim_num, ndata, tdata, ydata, tval, yval
        surf(j+1,i) = yval
      else
        surf(j+1,i) = notanum
      endif
    end do
  end do

end

subroutine interpolate( n_dat, n_int, x_dat, y_dat, x_int, y_int )
!
! arguments
!
  integer(kind=4), intent(in):: n_dat, n_int
  real(kind=8), intent(in):: x_dat(n_dat), y_dat(n_dat), x_int(n_int)
  real(kind=8), intent(out):: y_int(n_int)

! local variables
!
  real(kind=8):: fact
  integer(kind=4):: A, B

  do i=1, n_int
    ! Find the first interpolation interval
    find: do A=1, n_dat-1
            if (x_int(i) <= x_dat(A+1)) then
              exit find
!             else
!               A = A + 1
            endif
    end do find
!     write(*,*) A
    B = A + 1

    ! Extrapolation proof
    if (A >= n_dat) then
      y_int(i) = y_dat(A)
    else
      ! Interpolate
      fact = (x_int(i) - x_dat(A)) / (x_dat(B) - x_dat(A))
      y_int(i) = y_dat(A) + (y_dat(B) - y_dat(A)) * fact
    endif
  end do

end subroutine interpolate





