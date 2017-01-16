"""define the base models for the project"""
from django.db import models
from django.db.models import Q

PIN_MODES = (
    (0, 'Input'),
    (1, 'Output')
)

PIN_LEVELS = (
    (1, 'High'),
    (0, 'Low')
)

SONOFF_PIN_IDS = (
    (12, 'RELAY'),
    (13, 'LED_BUILTIN'),
    (14, 'DHT_PIN')
)

PIN_IDS = (
    (2, 'LED_BUILTIN'),
    (16, 'D0'),
    (5, 'D1'),
    (4, 'D2'),
    (0, 'D3'),
    (2, 'D4'),
    (14, 'D5'),
    (12, 'D6'),
    (13, 'D7'),
    (15, 'D8'),
    (3, 'RX'),
    (1, 'TX')
)

READING_TYPES = (
    (0, 'Humidity'),
    (1, 'Temperature'),
    (2, 'Heat Index')
)

READING_UNITS = (
    (0, 'Percent'),
    (1, 'Celcius'),
    (2, 'Fahrenheit'),
    (3, 'Felt Air C'),  # the heat index (feels like xxx deg C)
    (4, 'Felt Air F')  # the heat index (feels like xxx deg F)
)

READING_ABBR = (
    (0, '%'),
    (1, 'C'),
    (2, 'F'),
    (3, '*C'),  # the heat index (feels like xxx deg C)
    (4, '*F'),  # the heat index (feels like xxx deg F)
)


class D1Mini(models.Model):
    """defines a device"""
    mac_id = models.CharField(max_length=18)
    alias = models.CharField(max_length=50, null=True)
    has_dht = models.SmallIntegerField(default=0)
    LastHeard = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.mac_id

    @classmethod
    def create(cls, mac_id):
        """used to instantiate a new D1Mini, not sure we need this but
           some website suggested it would solve a problem.
           need fo find usages"""
        d1_mini = cls(
            mac_id=mac_id
        )
        return d1_mini


class Controllable(models.Model):
    """administrative configuration to constrain and define
       the controllable capabilityof a device"""
    device = models.ForeignKey(D1Mini)
    # mask of digital pins that can be controlled
    digital_controls = models.CharField(max_length=32)

    def __str__(self):
        return self.device.mac_id

    @classmethod
    def create(cls, mini, controllable_pins):
        """used to instantiate a controllable object"""
        controllable = cls(
            device=mini,
            digital_controls=controllable_pins
        )
        return controllable


class DigitalState(models.Model):
    """stores the state of a digital pin
       commands are used to invoke change
       events reported from the device can also lead to updates"""
    device = models.ForeignKey(D1Mini)
    pin_id = models.SmallIntegerField(default=-1)
    alias = models.CharField(max_length=50)
    is_high = models.BooleanField(default=False)
    is_inverse = models.BooleanField(default=False)

    def __str__(self):
        return self.device.mac_id

    @classmethod
    def create(cls, device_new, pin_id_new, alias_new, is_high_new, is_inverse_new):
        """used to instantiate a new DigitalState"""
        state = cls(
            device=device_new,
            pin_id=pin_id_new,
            alias=alias_new,
            is_high=is_high_new,
            is_inverse=is_inverse_new
        )
        return state


class D1MiniCommand(models.Model):
    """this is meant to tell the device what to do"""
    device = models.ForeignKey(D1Mini)
    pin_id = models.IntegerField(choices=PIN_IDS)
    pin_mode = models.SmallIntegerField(default=0, choices=PIN_MODES)
    pin_level = models.SmallIntegerField(default=0, choices=PIN_LEVELS)
    date_command = models.DateTimeField(auto_now=True, blank=True, null=True)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return "pk={0}".format(self.pk)

    @classmethod
    def create(cls,
               device,
               pin_id,
               pin_mode, pin_level, date_command=None,
               acknowledged=0):
        """used to instantiate new object"""
        d1_mini_command = cls(
            device=device,
            pin_id=pin_id,
            pin_mode=pin_mode,
            pin_level=pin_level,
            date_command=date_command,
            acknowledged=acknowledged
        )
        return d1_mini_command


class D1MiniEvent(models.Model):
    """define events that can take place on the device"""
    device = models.ForeignKey(D1Mini)
    pin_id = models.IntegerField(choices=PIN_IDS)
    pin_mode = models.SmallIntegerField(default=0, choices=PIN_MODES)
    pin_level = models.SmallIntegerField(default=0, choices=PIN_LEVELS)
    date_command = models.DateTimeField(auto_now=True, blank=True, null=True)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return "pk={0}".format(self.pk)

    @classmethod
    def create(cls,
               device,
               pin_id,
               pin_mode, pin_level, date_command=None,
               acknowledged=0):
        """used to instantiate a new D1Mini, not sure we need this but
        some website suggested it would solve a problem.
        need fo find usages"""
        d1_mini_event = cls(
            device=device,
            pin_id=pin_id,
            pin_mode=pin_mode,
            pin_level=pin_level,
            date_command=date_command,
            acknowledged=acknowledged
        )
        return d1_mini_event


class D1MiniReadingManager(models.Manager):
    """exposes some useful filters on readings"""

    def humidity_readings_for_mini(self, mini):
        """Return a queryset of humidity readings for a pk"""
        return super(D1MiniReadingManager, self).get_queryset().filter(
            Q(reading_type=0) & Q(device=mini))

    def temp_readings_for_mini(self, mini, reading_unit):
        """Return a queryset of humidity readings for a pk"""
        return super(D1MiniReadingManager, self).get_queryset().filter(
            Q(reading_type=1) & Q(reading_unit=reading_unit) & Q(device=mini))

    def felt_temp_readings_for_mini(self, mini, reading_unit):
        """Return a queryset of humidity readings for a pk"""
        return super(D1MiniReadingManager, self).get_queryset().filter(
            Q(reading_type=2) & Q(reading_unit=reading_unit) & Q(device=mini))


class D1MiniReading(models.Model):
    """define events that can take place on the device"""
    device = models.ForeignKey(D1Mini)
    reading_type = models.IntegerField(choices=READING_TYPES)
    reading_value = models.IntegerField(default=0)
    reading_unit = models.IntegerField(choices=READING_UNITS)
    date_reading = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "pk={0}".format(self.pk)

    @classmethod
    def create(cls,
               device,
               reading_type,
               reading_value, reading_unit, date_reading=None):
        """used to track telemetry like DHT, light sensors, etc"""
        d1_mini_reading = cls(
            device=device,
            reading_type=reading_type,
            reading_value=reading_value,
            reading_unit=reading_unit,
            date_reading=date_reading
        )
        return d1_mini_reading

    objects = D1MiniReadingManager()


class KeyStore(models.Model):
    """I need a way to store credentials and other details
    rather than have them in config files i'll store them in the db"""
    key_name = models.CharField(max_length=50)
    key_value = models.CharField(max_length=200)

    def __str__(self):
        return "pk={0}".format(self.pk)

    @classmethod
    def create(cls,
               key_name,
               key_value):
        """used to store and edit key value pairs"""
        key_entry = cls(
            key_name=key_name,
            key_value=key_value
        )
        return key_entry

