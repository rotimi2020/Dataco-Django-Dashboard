from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import SupplyChainRecord


@receiver(post_save, sender=SupplyChainRecord, dispatch_uid="dataco_clear_cache_on_save")
@receiver(post_delete, sender=SupplyChainRecord, dispatch_uid="dataco_clear_cache_on_delete")
def clear_dashboard_cache(sender, **kwargs):
    """Refresh cached analytics after a record is added, edited, or deleted."""
    cache.clear()
