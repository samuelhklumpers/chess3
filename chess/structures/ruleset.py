import threading
import bisect
import time
import traceback

class Ruleset:
    def __init__(self, game):
        self.game = game
        self.size = 0
        self.rules = {}
        self.watches = {"all": []}
        self.lock = threading.RLock()

        self.debug = False
        self.timeout = 0.0

    def add_rule(self, rule, prio=1):  # 0 first forbidden/debug, -1 last forbidden/debug
        self.rules.setdefault(prio, []).append(rule)

        if prio < 0:
            prio = 1000 - prio  # TODO

        for w in rule.watch:
            l = self.watches.setdefault(w, [])

            tup = (prio, self.size, rule)

            l.insert(bisect.bisect(l, tup), tup)

        self.size += 1

    def add_all(self, rules, prio=1):
        for rule in rules:
            self.add_rule(rule, prio=prio)

    def remove_rule(self, rule):
        for k in self.rules:
            if rule in self.rules[k]:
                self.rules[k].remove(rule)

        for w in rule.watch:
            if rule in self.watches.get(w, []):
                self.watches[w].remove(rule)

    def process_all(self, elist):
        try:
            for effect, args in elist:
                self.process(effect, args)
        except ValueError as e:
            raise e

    def process(self, effect, args):
        try:
            with self.lock:
                self._process(effect, args)
        except KeyboardInterrupt:
            print("Interrupted")

    def _process(self, effect, args):
        if self.debug:
            print(effect, args)
            time.sleep(self.timeout)

        views = self.watches.get(effect, []) + self.watches.get("all", [])
        views.sort()

        consequences = []
        prio2 = -1
        for prio, i, rule in views:
            if prio != prio2:
                prio2 = prio

                self.process_all(consequences)
                consequences = []
            
            if self.debug:
                ... #print(rule)

            res = None
            try:
                res = rule.process(self.game, effect, args)
            except:
                traceback.print_exc()

            if res is not None:
                res = list(res)
                consequences += res

        self.process_all(consequences)


__all__ = ["Ruleset"]