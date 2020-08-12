######################################
#
# Lottery Bot V2 Lottery Validator
# Python Version
#
# Author: EQblog <i@en.mk> https://github.com/eqblog
# License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
#
######################################


import requests
import hashlib
import sys


class lottery:
    def __init__(self, lottery_id):
        self.lottery_id = lottery_id
        self.gift_count = 0
        self.uids = []
        self.user_count = 0
    
    def Sort_By_Ascii(self):
        sort_uids = []
        sort_uids = sorted(self.uids, reverse=True)
        return sort_uids

    def Get_Api(self):
        try:
            req=requests.get("https://lottery.tg/lottery/{}/data".format(self.lottery_id),timeout=10).json()
        except:
            return 0
        return req
    def Get_uid(self,data):
        uids=[]
        for i in data['data']['joined_list']:
            if not i['ineligible']:
                uids.append(i['hash'])
        return uids
    def Gen_Seeds(self, block_hash):
        return self.Encode_Sha256(self.lottery_id+str(self.user_count)+str(self.gift_count)+block_hash)
    def Get_User(self, sort_uids, seeds):
        end_user = []
        while True:
            if len(end_user) < self.gift_count:
                key = int(seeds, 16) % self.user_count
                if sort_uids[key] not in end_user:
                    end_user.append(sort_uids[key])
                seeds = self.Encode_Sha256(seeds)
            else:
                return end_user

    def Gift_Ass(self, gfit_list ,end_user):
        gift_sort=[]
        user=[]
        for gfit in gfit_list:
            for i in range(gfit['amount']):
                gift_sort.append(gfit['name'])
        for k,v in enumerate(end_user):
            user.append({'gfit':gift_sort[k],'user':v})
        return user

    def Encode_Sha256(self, strings):
        hash = hashlib.sha256()
        hash.update(strings.encode('utf-8'))
        return hash.hexdigest()


if __name__ == "__main__":
    '''
    Example
    '''
    lottery_id = sys.argv[1]
    user_id = sys.argv[2]
    exp = lottery(lottery_id)
    user_hash=exp.Encode_Sha256(str(user_id)+str(lottery_id))
    api_data=exp.Get_Api()
    if api_data!=0:
        exp.gift_count=api_data['data']['gift_amount']
        exp.uids=exp.Get_uid(api_data)
        if user_hash in exp.uids:
            exp.user_count=len(exp.uids)
            sort_uid = exp.Sort_By_Ascii()
            sort_uids = sort_uid
            block_hash = api_data['data']['block_hash']
            seeds = exp.Gen_Seeds(block_hash)
            end_user = exp.Get_User(sort_uids, seeds)
                #print(exp.Gift_Ass(api_data['data']['gifts'], end_user))
            '''
                print format
            '''
            print('''Lottery: {}
Ethereum Block: {} ({})
Your Hash: {}
Lucky Hash:'''.format(api_data['data']['lottery_id'],api_data['data']['block_height'],api_data['data']['block_hash'],user_hash))
            for i in exp.Gift_Ass(api_data['data']['gifts'], end_user):
                if i['user']==user_hash:
                    giftisyourschar="(You) "
                else:
                    giftisyourschar=""
                print("- {}{} - {}".format(giftisyourschar,i['user'],i['gfit']))
        else:
            print('user id error')
    else:
        print("api error")
