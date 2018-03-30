"""
Tests for MailingList class
"""

import pandas
from mailinglist import MailingList

ML1 = MailingList('data/test_thread2.csv')
ML2 = MailingList('data/test_sample1.csv')


class TestMakeThreads(object):
    """Test number of emails tagged with correct thread id"""

    ML1.make_threads()
    ML2.make_threads()

    def test_number_of_threads(self):
        assert len(ML2.emails.thread.unique()) == 41
        assert len(ML1.emails.thread.unique()) == 1

    def test_number_of_emails_in_thread(self):
        assert len(ML1.emails[ML1.emails.thread == 'tnxy899zzu7.fsf@arm.com']) == 15
        assert len(ML2.emails[ML2.emails.thread == '20170520214233.7183-1-avarab@gmail.com']) == 55


class TestProcessThreads(object):

    ML1.process_threads()
    ML2.process_threads()

    def test_threads_msgids(self):
        assert set(ML1._threads.keys()) == set(['tnxy899zzu7.fsf@arm.com'])
        assert set(ML2._threads.keys()) == set([
            '0E82EDCE97D80143A03AE87B9DF4EB3A8A7E8CD7@Sydmail.civica.com.au',
            '15c2318a2c4.1100a44f3621653.6175207833450352995@calebevans.me',
            '20170519024451.11252-1-kyle@kyleam.com',
            '20170519172856.GA14673@blind.goeswhere.com',
            '20170520055216.30470-1-git-dpa@aegee.org',
            '20170520203649.GA13079@untitled',
            '20170520214233.7183-1-avarab@gmail.com',
            '20170521025604.GA8068@csmail.ucc.ie',
            '20170521122711.22021-1-pc44800@gmail.com',
            '20170521125950.5524-1-zxq_yx_007@163.com',
            '20170522135001.54506-1-larsxschneider@gmail.com',
            '20170522190114.19832-1-sbeller@google.com',
            '20170522194533.6394-1-asheiduk@gmail.com',
            '20170522194806.13568-1-sbeller@google.com',
            '20170522205958.10962-1-asheiduk@gmail.com',
            '20170524051537.29978-1-whydoubt@gmail.com',
            '20170525152739.t63dbsq2dojy2y2h@sigill.intra.peff.net',
            '20170525183612.3128-1-benpeart@microsoft.com',
            '20170525193304.fhtmywv4xisclhii@sigill.intra.peff.net',
            '20170525194535.9324-1-avarab@gmail.com',
            '20170525200528.22037-1-avarab@gmail.com',
            '20170525232046.3421-1-szeder.dev@gmail.com',
            '4a5619af-d695-ab6c-e603-368e38827455@ramsayjones.plus.com',
            '578bfb5b-bdd1-a418-98f2-d26e1bff0be2@ramsayjones.plus.com',
            '76491764-cd43-ef7f-fbfc-939a15f2fb77@onlinehome.de',
            'BLUPR0701MB75463EE0B8ADC559BBE02A282F90@BLUPR0701MB754.namprd07.prod.outlook.com',
            'CAAZatrCaoB7EXVrCvC9RKmO02G5xcp8GPBaJefHfv7zAXVpL3Q@mail.gmail.com',
            'CACBZZX41yrAtBvkVeL9Q=2_TxcwrDXh55gu3qLN54P_go318OA@mail.gmail.com',
            'CACQm2Y1QtKD3M6weNhGrAQSLV8hLF4pKcpHDD7iUc78aWrt6Cw@mail.gmail.com',
            'CACfpxdthS4W9giaFNd7GVxPw4BMJ85GmOQAJbEL84YHrouyK9Q@mail.gmail.com',
            'CAGZ79kYirjV0eQgB_ng-64HSPN_7njUMjnoNBkmWnx-rinsemQ@mail.gmail.com',
            'CAHd499B+cyN=3XDqr7KgHSpyHLwi6bS=P_4beoS5fSkFhapAtw@mail.gmail.com',
            'CAJtFkWu25RkiKm0O__W2My+Adi9pxZ3YtjZW4eb+2U+wpNS3yA@mail.gmail.com',
            'CAME+mvUJSdEyvNho=WwC+9gXaG7_emoHEACznx2goFzPp+t+KA@mail.gmail.com',
            'CAOJu4w-4eCkt9Co19BmyTQ7NF+rf23LU8ANCTCcmPP84efdjeA@mail.gmail.com',
            'CAPZ477MCsBsfbqKzp69MT_brwz-0aes6twJofQrhizUBV7ZoeA@mail.gmail.com',
            'c5b7292f-6367-e4a9-2ee0-96b93b1b587f@web.de',
            'cover.1495261020.git.j6t@kdbg.org',
            'cover.1495460199.git.mhagger@alum.mit.edu',
            'xmqqo9ulo1yn.fsf@gitster.mtv.corp.google.com',
            'xmqqwp98j8q2.fsf@gitster.mtv.corp.google.com',
        ])

    def test_sum_thread_email_number(self):
        assert ML1.threads.emails.sum() == 15
        assert ML2.threads.emails.sum() == 321
