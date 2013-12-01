import webapp2
from datetime import datetime, timedelta
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
        B_keys    = ndb.put_multi(B)
        now       = datetime.now()
        yesterday = now - timedelta(1)
        tomorrow  = now + timedelta(1)

        C = [
            Coupon(
                business=B_keys[0],
                name='Free Guacamole',
                description='Don\'t pay any extra to add guacamole to your order',
                start=yesterday+timedelta(0,100),
                end=tomorrow+timedelta(0,100)
            ),
            Coupon(
                business=B_keys[1],
                name='Something completely different',
                start=yesterday+timedelta(0,200),
                end=tomorrow
            ),            
            Coupon(
                business=B_keys[1],
                name='50% off coffee',
                description='Today\'s old coffee at half price',
                start=yesterday+timedelta(0,500),
                end=tomorrow+timedelta(0,100)
            ),
            Coupon(
                business=B_keys[2],
                name='Lorem ipsum dolor sit amet',
                description='Sed quis est ac nulla scelerisque sagittis in a arcu. Cras quis nulla in lectus iaculis varius. Nulla sollicitudin, enim in tincidunt cursus, mi urna mollis diam, et dignissim massa eros ut purus. Donec sit amet elit gravida, porta tortor quis, lacinia neque.',
                start=yesterday,
                end=tomorrow+timedelta(0,100)
            ),
            Coupon(
                business=B_keys[2],
                name='Suspendisse ligula urna',
                description='Dapibus egestas tempor sit amet, consectetur ut quam. Suspendisse lacinia eros adipiscing, consequat justo id, bibendum augue. Aliquam eu tincidunt leo.',
                start=yesterday+timedelta(0,200),
                end=tomorrow+timedelta(0,200)
            ),
            Coupon(
                business=B_keys[2],
                name='Donec ac ante sit amet arcu elementum tempor',
                description='Etiam ullamcorper sagittis mattis. Aenean ante ante, consequat ac mauris ut, aliquet venenatis nibh. Sed eget lacus quis lacus ornare imperdiet vitae eu magna. Donec ultrices, nunc in viverra ornare, felis tortor congue leo, id hendrerit turpis tellus eu orci. ',
                start=yesterday+timedelta(0,300),
                end=tomorrow+timedelta(0,300)
            ),
            Coupon(
                business=B_keys[2],
                name='Morbi pretium luctus purus eget egestas',
                description='Duis sit amet sollicitudin lectus. Suspendisse vel scelerisque justo, vitae interdum sapien. Pellentesque adipiscing nec ante sit amet ornare. Proin eget condimentum dui. Sed pulvinar auctor fermentum. Maecenas lacinia eleifend ligula consequat interdum. Pellentesque in vehicula enim, nec dapibus tellus. Nam rhoncus dignissim risus, nec lacinia lacus molestie nec.',
                start=yesterday,
                end=tomorrow
            ),
            Coupon(
                business=B_keys[2],
                name='Proin vehicula odio est',
                description='Vivamus dictum at risus a venenatis. Fusce varius, tortor ac sollicitudin placerat, est neque elementum tellus, a pretium risus tellus ut dolor. Donec imperdiet turpis quis nulla rhoncus tristique.',
                start=tomorrow,
                end=tomorrow+timedelta(1)
            ),
            Coupon(
                business=B_keys[2],
                name='Nulla tincidunt placerat neque vel viverra',
                description='Donec pretium tellus est, vel rhoncus nunc volutpat a. Nunc eleifend quam et lorem cursus aliquet. Nunc diam magna, viverra sodales volutpat tempor, venenatis a dui. Nunc varius elementum commodo. Vestibulum pretium felis ac accumsan convallis. Aenean sodales lobortis purus non blandit.',
                start=tomorrow+timedelta(0.5),
                end=tomorrow+timedelta(1.5)
            ),
            Coupon(
                business=B_keys[2],
                name='Morbi quis odio sapien',
                description='Mauris at purus lobortis, lacinia sem sed, tempus ipsum. Curabitur enim magna, varius id arcu id, consequat feugiat dolor. Vivamus luctus, mauris eget accumsan pharetra, purus elit lobortis orci, imperdiet scelerisque lorem massa non ante.',
                start=yesterday-timedelta(1),
                end=now
            ),
            Coupon(
                business=B_keys[2],
                name='Cras auctor pulvinar luctus',
                description='Proin convallis vulputate vehicula. Aliquam nec tincidunt urna. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Proin mollis ante id lorem vehicula, a ultricies justo mattis. Nulla pretium sollicitudin dui, fringilla ullamcorper lacus aliquet ac. Quisque imperdiet malesuada mauris, eu porttitor quam adipiscing ac.',
                start=yesterday-timedelta(2),
                end=yesterday-timedelta(1)
            )
        ]
        C_keys = ndb.put_multi(C)
        U = [
            User(
                surname='Araxa',
                familiar_name='Da\'Vas',
                email='DaVasAraxa@teleworm.us',
                phone=7704505687,
                address=Address(
                    number=2975,
                    street='Elk Creek Road',
                    city='Norcross',
                    state='GA',
                    zip=30071
                )
            )
        ]
        U_keys = ndb.put_multi(U)
        self.response.write('success')

    def get(self):
        for b in Business.query().iter():
            b.key.delete()
        for c in Coupon.query().iter():
            c.key.delete()
        self.init()