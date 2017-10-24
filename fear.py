# pylint: disable=no-member,unused-variable,unused-import
from math import pi

from kivy.factory import Factory
from kivy.logger import Logger  # noqa: F401
from kivy.properties import NumericProperty
from kivent_core.systems.gamesystem import GameSystem
import numpy as np

import defs

# def debug_F(f):
#     w, h = f.shape
#     from matplotlib import pyplot as plt
#     from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     ax.set_zlim(-10, 1000)
#     X = np.arange(w)
#     Y = np.arange(h)
#     X, Y = np.meshgrid(X, Y)
#     ax.plot_wireframe(X, Y, f, rstride=10, cstride=10)
#     plt.show()


class Fear(GameSystem):
    granulity = NumericProperty(6)

    # static data
    pre_computed_fields = {}

    def init_component(self, cindex, eid, zone, args):
        if 'attraction' not in args:
            args['attraction'] = None
        if 'repulsion' not in args:
            args['repulsion'] = None
        if 'safety' not in args:
            args['safety'] = None
        if 'nomove' not in args:
            args['nomove'] = False

        super(Fear, self).init_component(cindex, eid, zone, args)
        comp = self.components[cindex]
        comp.courage = 1.0
        comp.stone_contact = False

    def on_add_system(self):
        gw = self.gameworld
        gw.phy.add_collision_handler(defs.coltype_rat,
                                                defs.coltype_stone,
                                                begin_func=self.rat_vs_stone_begin,
                                                separate_func=self.rat_vs_stone_end)

    def rat_vs_stone_begin(self, _space, arbiter):
        srat, sstone = arbiter.shapes
        assert srat.collision_type, sstone.collision_type == (2, 3)
        erat = srat.body.data

        crat = self.components[erat]
        crat.stone_contact = True

    def rat_vs_stone_end(self, _space, arbiter):
        srat, sstone = arbiter.shapes
        assert srat.collision_type, sstone.collision_type == (2, 3)
        erat = srat.body.data

        crat = self.components[erat]
        crat.stone_contact = False

    def entity(self, comp):
        if comp is None:
            return None
        return self.gameworld.entities[comp.entity_id]

    def update(self, _dt):

        velxs = np.zeros(len(self.components))
        velys = np.zeros(len(self.components))
        entities = [self.entity(c) for c in self.components]
        xposs = np.array([e.position.pos[0] for e in entities])
        yposs = np.array([e.position.pos[1] for e in entities])
        courages = np.array([c.courage for c in self.components])

        for c2 in self.components:
            if c2.attraction is None and c2.repulsion is None and c2.safety is None:
                continue

            e2 = self.entity(c2)

            vecxs = xposs - e2.position.pos[0]
            vecys = yposs - e2.position.pos[1]
            dist2s = vecxs**2 + vecys**2

            if c2.safety:
                velxs -= vecxs * c2.safety / dist2s / courages
                velys -= vecys * c2.safety / dist2s / courages

            if c2.attraction:
                velxs -= vecxs * c2.attraction / dist2s * courages
                velys -= vecys * c2.attraction / dist2s * courages

            if c2.repulsion:
                velxs += vecxs * c2.repulsion / dist2s / courages
                velys += vecys * c2.repulsion / dist2s / courages

        vellengths = np.sqrt(velxs**2 + velys**2)
        dvelxs = velxs / vellengths * defs.rat_speed
        dvelys = velys / vellengths * defs.rat_speed
        angles = np.arctan2(dvelys, dvelxs) + pi/2

        for c, e, velx, vely, angle in zip(self.components, entities, dvelxs, dvelys, angles):
            if c.nomove:
                continue
            e.cymunk_physics.body.velocity = (velx, vely)
            e.rotate.r = angle

        for c in self.components:
            # courage things
            if c.stone_contact:
                c.courage *= 1.05
            else:
                c.courage *= 0.99


Factory.register('Fear', cls=Fear)
