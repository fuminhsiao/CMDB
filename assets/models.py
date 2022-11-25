from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Asset(models.Model):
    asset_type_choice = (
        ('server', 'Server'),
        ('networkdevice', 'Network Device'),
        ('storagedevice', 'Storage Device'),
        ('securitydevice', 'Security Device'),
        ('software', 'Software'),

    )

    asset_status = (
        (0, 'online'),
        (1, 'offline'),
        (2, 'unknown'),
        (3, 'out of order'),
        (4, 'backup')
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name="Asset Type")
    name = models.CharField(max_length=64, unique=True, verbose_name="Asset Name")
    sn = models.CharField(max_length=128, unique=True, verbose_name="Asset Serial Number")
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name="Business Unit",
                                      on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='Asset Status')
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='Manufacturer',
                                     on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Management')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Tag')
    admin = models.ForeignKey(User, null=True, verbose_name='Asset Administrator', related_name='admin',
                              on_delete=models.SET_NULL)
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='IDC', on_delete=models.SET_NULL)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='Contract', on_delete=models.SET_NULL)

    purchase_day = models.DateField(null=True, blank=True, verbose_name='Purchase Day')
    expire_day = models.DateField(null=True, blank=True, verbose_name='Expire Day')
    price = models.FloatField(null=True, blank=True, verbose_name='Price')

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='Approved By', related_name='approved_by',
                                    on_delete=models.SET_NULL)

    memo = models.TextField(null=True, blank=True, verbose_name='Memo')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='Approved Date')
    m_time = models.DateTimeField(auto_now=True, verbose_name='Updated Date')

    def __str__(self):
        return '<%s> %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = 'Assets Sheet'
        verbose_name_plural = 'Assets Sheets'
        ordering = ['-c_time']


class Server(models.Model):
    sub_asset_type_choice = (
        (0, 'PC Server'),
        (1, 'Blade Server'),
        (2, 'Mini Server'),
    )

    created_by_choice = (
        ('auto', 'Auto Add'),
        ('manual', 'Manual Add'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='Server Type')
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name='Add Method')
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True,
                                  verbose_name="Host on Server", on_delete=models.CASCADE)
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='Server Model')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid Type')

    os_type = models.CharField('OS Type', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('OS Distribution', max_length=64, blank=True, null=True)
    os_release = models.CharField('OS version', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'


class SecurityDevice(models.Model):
    sub_asset_type_choice = (
        (0, 'Firewall'),
        (1, 'Attack detection device'),
        (2, 'Internet Gateway'),
        (3, 'Cloud Bastion Host'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0,
                                              verbose_name='Security Device Type')
    model = models.CharField(max_length=128, default='unknown', verbose_name='Security Device Model')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = 'Security Device'
        verbose_name_plural = 'Security Devices'


class StorageDevice(models.Model):
    sub_asset_type_choice = (
        (0, 'Raid'),
        (1, 'NAS'),
        (2, 'Tape Library'),
        (3, 'Tape Drive'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0,
                                              verbose_name='Storage Device Type')
    model = models.CharField(max_length=128, default='unknown', verbose_name='Storage Device Model')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = 'Storage Device'
        verbose_name_plural = 'Storage Devices'


class NetworkDevice(models.Model):
    sub_asset_type_choice = (
        (0, 'Router'),
        (1, 'Switch'),
        (2, 'Load Balancing'),
        (3, 'VPN Device'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0,
                                              verbose_name='Network Device Type')
    model = models.CharField(max_length=128, default='unknown', verbose_name='Network Device Model')

    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='Intranet IP')

    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name='Firmware Version')
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="Port Number")
    device_detail = models.TextField(null=True, blank=True, verbose_name='Device Detail')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = 'Network Device'
        verbose_name_plural = 'Network Devices'


class Software(models.Model):
    sub_asset_type_choice = (
        (0, 'OS'),
        (1, 'Office/Develop Software'),
        (2, 'Business Software'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0,
                                              verbose_name='Software Type')
    license_num = models.IntegerField(default=1, verbose_name='authorized license')
    version = models.CharField(max_length=64, unique=True, help_text='Example: RedHat release 7 (Final)',
                               verbose_name='Software version')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = 'Software'
        verbose_name_plural = 'Software'


class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="IDC Name")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='Memo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'IDC'
        verbose_name_plural = 'IDCs'


class Manufacturer(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Manufacturer Name")
    telephone = models.CharField('Support Phone Number', max_length=30, blank=True, null=True)
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='Memo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'


class BusinessUnit(models.Model):
    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level',
                                    on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, unique=True, verbose_name="Business Name")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='Memo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Business Line'
        verbose_name_plural = 'Business Lines'


class Contract(models.Model):
    sn = models.CharField('Contract SN', max_length=128, unique=True)
    name = models.CharField('Contract Name', max_length=64)
    memo = models.TextField('Memo', blank=True, null=True)
    price = models.IntegerField('Contract Price')
    detail = models.TextField('Contract Details', blank=True, null=True)
    start_day = models.DateField('Start Day', blank=True, null=True)
    end_day = models.DateField('End Day', blank=True, null=True)
    license_num = models.IntegerField('Licence Number', blank=True, null=True)
    c_day = models.DateField('Create Date', auto_now_add=True)
    m_day = models.DateField('Modify Date', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'


class Tag(models.Model):
    name = models.CharField('Tag Name', max_length=32, unique=True)
    c_day = models.DateField('Create Date', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class CPU(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField('CPU Model', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('CPU Number', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('CPU Core Number', default=1)

    def __str__(self):
        return self.asset.name + ":  " + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPUs'


class RAM(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('RAM SN', max_length=128, blank=True, null=True)
    model = models.CharField('RAM Model', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('RAM Manufacturer', max_length=128, blank=True, null=True)
    slot = models.CharField('Slot', max_length=64)
    capacity = models.IntegerField('RAM Capacity(GB)', blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAM'
        unique_together = ('asset', 'slot')


class Disk(models.Model):
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('Disk SN', max_length=128)
    slot = models.CharField('Disk Slot', max_length=128, blank=True, null=True)
    model = models.CharField('Disk Model', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('Disk Manufaturer', max_length=128, blank=True, null=True)
    capacity = models.FloatField('Disk Capacity(GB)', blank=True, null=True)
    interface_type = models.CharField('Interface Type', max_length=16, choices=disk_interface_type_choice,
                                      default='unknown')

    def __str__(self):
        return '%s: %s: %s: %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = 'Disk'
        verbose_name_plural = 'Disk'
        unique_together = ('asset', 'sn')


class NIC(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField('NIC Name', max_length=64, blank=True, null=True)
    model = models.CharField('NIC Model', max_length=128)
    mac = models.CharField('MAC Address', max_length=64)
    ip_address = models.GenericIPAddressField('IP Address', blank=True, null=True)
    net_mask = models.CharField('Net Mask', max_length=64, blank=True, null=True)
    bonding = models.CharField('Bonding', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = 'NIC'
        verbose_name_plural = 'NIC'
        unique_together = ('asset', 'model', 'mac')


class EventLog(models.Model):
    name = models.CharField('Event Log', max_length=128)
    event_type_choice = (
        (0, 'others'),
        (1, 'hardware change'),
        (2, 'add accessories'),
        (3, 'asset offline')
    )

    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField('Event Type', choices=event_type_choice, default=0)
    component = models.CharField('Event Component', max_length=256, blank=True, null=True)
    detail = models.TextField('Event Details')
    date = models.DateTimeField('Event Time', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Event Executor', on_delete=models.SET_NULL)
    memo = models.TextField('Memo', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event Log'
        verbose_name_plural = 'Event Log'


class NewAssetApprovalZone(models.Model):
    sn = models.CharField('Asset SN', max_length=128, unique=True)
    asset_type_choice = (
        ('server', 'Server'),
        ('networkdevice', 'Network Device'),
        ('storagedevice', 'Storage Device'),
        ('securitydevice', 'Security Device'),
        ('software', 'Software'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='Asset Type')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='Asset Manufacturer')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='Asset Model')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='RAM Size')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU Model')
    cpu_count = models.PositiveSmallIntegerField('CPU Count', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField('CPU Core Count', blank=True, null=True)
    os_distribution = models.CharField('OS Distribution', max_length=64, blank=True, null=True)
    os_type = models.CharField('OS type', max_length=64, blank=True, null=True)
    os_release = models.CharField('OS version', max_length=64, blank=True, null=True)

    data = models.TextField('Asset Data')

    c_time = models.DateTimeField('Asset create time', auto_now_add=True)
    m_time = models.DateTimeField('Asset Modify time', auto_now=True)
    approved = models.BooleanField('Approval Status', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = 'New Asset Approval'
        verbose_name_plural = 'New Asset Approval'
        ordering = ['-c_time']

# Create your models here.
