import webapp2
import datetime
from google.appengine.ext import ndb
from models import Business, Coupon, User, Address


class InitHandler(webapp2.RequestHandler):
    def init(self):
        B = [
            Business(
                name='Chipotle',
                lat=35.945841,
                lon=-86.825259,
                address=Address(
                    number=430,
                    street='Cool Springs Blvd',
                    city='Franklin',
                    state='TN',
                    zip=37067
                )
            ),
            Business(
                name='Dunkin\' Donuts',
                lat=35.959632,
                lon=-86.801355,
                address=Address(
                    number=9100,
                    street='Carothers Pkwy',
                    city='Franklin',
                    state='TN',
                    zip=37067
                )
            ),
            Business(
                name='Starbucks',
                lat=35.960119,
                lon=-86.802725,
                address=Address(
                    number=430,
                    street='Cool Springs Blvd',
                    city='Franklin',
                    state='TN',
                    zip=37067
                )
            )
        ]
        B_keys = ndb.put_multi(B)
        now       = datetime.datetime.now()
        yesterday = now - datetime.timedelta(1)
        tomorrow  = now + datetime.timedelta(1)
        C = [
            Coupon(
                business=B_keys[0],
                name='Free Guacamole',
                description='Don\'t pay any extra to add guacamole to your order',
                start=yesterday,
                end=tomorrow
            ),
            Coupon(
                business=B_keys[1],
                name='Something completely different',
                start=yesterday,
                end=tomorrow
            ),            
            Coupon(
                business=B_keys[1],
                name='50% off coffee',
                description='Today\'s old coffee at half price',
                start=yesterday,
                end=tomorrow
            ),
            Coupon(
                business=B_keys[2],
                name='Lorem ipsum dolor sit amet',
                description='Sed quis est ac nulla scelerisque sagittis in a arcu. Cras quis nulla in lectus iaculis varius. Nulla sollicitudin, enim in tincidunt cursus, mi urna mollis diam, et dignissim massa eros ut purus. Donec sit amet elit gravida, porta tortor quis, lacinia neque.',
                start=yesterday,
                end=tomorrow
            ),
            Coupon(
                business=B_keys[2],
                name='Suspendisse ligula urna',
                description='dapibus egestas tempor sit amet, consectetur ut quam. Suspendisse lacinia eros adipiscing, consequat justo id, bibendum augue. Aliquam eu tincidunt leo.',
                start=yesterday,
                end=tomorrow
            ),
            Coupon(
                business=B_keys[2],
                name='Donec ac ante sit amet arcu elementum tempor',
                description='Etiam ullamcorper sagittis mattis. Aenean ante ante, consequat ac mauris ut, aliquet venenatis nibh. Sed eget lacus quis lacus ornare imperdiet vitae eu magna. Donec ultrices, nunc in viverra ornare, felis tortor congue leo, id hendrerit turpis tellus eu orci. ',
                start=yesterday,
                end=tomorrow
            ),
            Coupon(
                business=B_keys[2],
                name='Morbi pretium luctus purus eget egestas',
                description='Duis sit amet sollicitudin lectus. Suspendisse vel scelerisque justo, vitae interdum sapien. Pellentesque adipiscing nec ante sit amet ornare. Proin eget condimentum dui. Sed pulvinar auctor fermentum. Maecenas lacinia eleifend ligula consequat interdum. Pellentesque in vehicula enim, nec dapibus tellus. Nam rhoncus dignissim risus, nec lacinia lacus molestie nec.',
                start=yesterday,
                end=tomorrow
            )
        ]
        ndb.put_multi(C)

    def get(self):
        for b in Business.query().iter():
            b.key.delete()
        for c in Coupon.query().iter():
            c.key.delete()
        for u in User.query().iter():
            u.key.delete()
        self.init()