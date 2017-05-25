from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import DisCountCoupon
from .forms import CouponApplyForm, CouponCreateForm
from django.contrib.auth.decorators import login_required
from shop.decorators import check_manager_dec
from django.core.urlresolvers import reverse

@login_required
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = DisCountCoupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except DisCountCoupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect(reverse('cart:cart_detail'))


@check_manager_dec
def coupon_create(request, shop_id):
    if request.method == 'POST':
        form = CouponCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('coupons:charge_coupon', args=[shop_id]))
    else:
        form = CouponCreateForm()
    context = {'form': form}
    return render(request, 'coupons/create_coupon.html', context)


@check_manager_dec
def charge_coupon(request, shop_id):
    shop = shop_id
    now = timezone.now()
    coupon_list = shop.discount_coupon_set.filter(active=True, valid_to__gte=now)
    context = {'coupon_list': coupon_list}
    return render(request, 'coupons/charge_coupon.html', context)