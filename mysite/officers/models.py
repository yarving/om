# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models


origin_choices = (
    ('市纪委', '市纪委'),
    ('市法院', '市法院'),
    ('市检察院', '市检察院'),
    ('市政法委', '市政法委'),
    ('市直属工委', '市直属工委'),
    ('省委巡视组', '省委巡视组'),
    ('市信访局', '市信访局'),
    ('市公安局', '市公安局'),
    ('市人社局', '市人社局'),
    ('市编办', '市编办'),
    ('市卫计委', '市卫计委'),
    ('市审计局', '市审计局'),
    ('市安监局', '市安监局'),
    ('市委组织部', '市委组织部'),
)

yes_or_no_choices = (
    ('是', '是'),
    ('否', '否'),
)


class Officer(models.Model):
    """docstring for Pool."""
    name = models.CharField('姓名', max_length=20)
    pub_date = models.DateTimeField('更新日期', null=True, blank=True)
    gender_choices = (
        ('男', '男'),
        ('女', '女'),
    )
    gender = models.CharField('性别', max_length=2,
                              choices=gender_choices,
                              default='男')
    birthday = models.DateField('出生日期')
    forbidden_start = models.DateField('影响提拔起始时间', null=True, blank=True)
    forbidden_end = models.DateField('影响提拔截止时间', null=True, blank=True)
    party_choices = (
        ('是', '是'),
        ('否', '否'),
    )
    is_party = models.CharField(
        '是否中共党员', max_length=2, choices=party_choices, default='是',
    )

    party_time = models.DateField('入党时间', null=True, blank=True)
    job_time = models.DateField('工作时间')
    native = models.CharField('籍贯', max_length=20, default='湖南永州')
    nation = models.CharField('民族', max_length=20, default='汉')
    duty_level_choices = (
        ('副科级领导干部', '副科级领导干部'),
        ('副科级非领导干部', '副科级非领导干部'),
        ('正科级领导干部', '正科级领导干部'),
        ('正科级非领导干部', '正科级非领导干部'),
        ('副处级领导干部', '副处级领导干部'),
        ('副处级非领导干部', '副处级非领导干部'),
        ('正处级领导干部', '正处级领导干部'),
        ('正处级非领导干部', '正处级非领导干部'),
        ('副厅级领导干部', '副厅级领导干部'),
        ('副厅级非领导干部', '副厅级非领导干部'),
    )
    duty_level = models.CharField(
        '职务层次', max_length=20, choices=duty_level_choices
    )
    id_number = models.CharField('身份证号', max_length=18, default='无')
    job_title = models.CharField('工作单位及职务', max_length=50, null=True)
    full_time_edu = models.CharField('全日制学历', max_length=10, null=True, default='大学')
    full_time_deg = models.CharField('全日制学位', max_length=10, null=True, default='未知')
    part_time_edu = models.CharField('在职学历', max_length=10, null=True, default='未知')
    part_time_deg = models.CharField('在职学位', max_length=10, null=True, default='未知')

    def __str__(self):
        return self.name

    def was_able_promotion(self):
        if (self.forbidden_end is None) or (self.forbidden_end is None):
            return True

        return not (self.forbidden_start <= datetime.datetime.now().date() <= self.forbidden_end)

    was_able_promotion.admin_order_field = 'forbidden_start'
    was_able_promotion.boolean = True
    was_able_promotion.short_description = '是否影响使用?'

    class Meta:
        verbose_name = '干部'
        verbose_name_plural = '市管干部信息'



class Choice(models.Model):
    """docstring for Choice."""
    officer = models.ForeignKey(Officer, verbose_name='干部')
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.choice


class Assessment(models.Model):
    """考核"""
    officer = models.ForeignKey(Officer, verbose_name='干部')
    year_choices = (
        ('2016', '2016'),
        ('2015', '2015'),
        ('2014', '2014'),
    )
    origin_choices = (
        ('市纪委', '市纪委'),
        ('市法院', '市法院'),
        ('市检察院', '市检察院'),
        ('市政法委', '市政法委'),
        ('市直属工委', '市直属工委'),
        ('省委巡视组', '省委巡视组'),
        ('市信访局', '市信访局'),
        ('市公安局', '市公安局'),
        ('市人社局', '市人社局'),
        ('市编办', '市编办'),
        ('市卫计委', '市卫计委'),
        ('市审计局', '市审计局'),
        ('市安监局', '市安监局'),
        ('市委组织部考核办', '市委组织部考核办'),
    )
    year = models.CharField('年度', max_length=4,
                            choices=year_choices,
                            default='2017')
    level_choices = (
        ('基本称职', '基本称职'),
        ('不称职', '不称职'),
        ('不定等', '不定等'),
    )
    level = models.CharField('评定等级', max_length=8,
                             choices=level_choices,
                             default='优秀')
    is_influence = models.CharField(
        '是否影响使用', max_length=4, choices=yes_or_no_choices, blank=True
    )
    start_time = models.DateField('影响起始时间', null=True, blank=True)
    end_time = models.DateField('影响终止时间', null=True, blank=True)
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices,
                              default='市委组织部考核办')

    def __str__(self):
        return self.officer.name + self.year + self.level

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(Assessment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '年度考核'
        verbose_name_plural = '年度考核称职情况'


class PersonalEvent(models.Model):
    """领导干部个人事项报告"""
    origin_choices = (
        ('纪委', '纪委'),
        ('法院', '法院'),
        ('检察院', '检察院'),
        ('市政法委', '市政法委'),
        ('直属工委', '直属工委'),
        ('巡视联络办', '巡视联络办'),
        ('信访局', '信访局'),
        ('公安局', '公安局'),
        ('人社局', '人社局'),
        ('市编办', '市编办'),
        ('计生', '计生'),
        ('审计', '审计'),
        ('安监', '安监'),
        ('市委组织部', '市委组织部'),
    )
    officer = models.ForeignKey(Officer, verbose_name='干部')
    index = models.CharField('核查批次', max_length=10)
    status = models.TextField('核查对比情况')
    express = models.TextField('本人说明及提供汇报情况')
    result = models.TextField('处理意见')
    is_influence = models.CharField(
        '是否影响使用', max_length=4, choices=yes_or_no_choices, blank=True)
    start_time = models.DateField('影响起始时间', null=True, blank=True)
    end_time = models.DateField('影响终止时间', null=True, blank=True)
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices,
                              default='市委组织部')

    def __str__(self):
        return self.officer.name + '-' + self.index

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(PersonalEvent, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '领导干部个人事项报告'


class EconomicReview(models.Model):
    """经济责任审查"""
    officer = models.ForeignKey(Officer, verbose_name='干部')
    status = models.TextField('审查基本情况')
    result = models.CharField('处理意见', max_length=20)
    is_influence = models.CharField(
        '是否影响使用', max_length=4, choices=yes_or_no_choices, blank=True)
    start_time = models.DateField('影响起始时间', null=True, blank=True)
    end_time = models.DateField('影响终止时间', null=True, blank=True)
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices)

    def __str__(self):
        return self.officer.name + '-' + self.status

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(EconomicReview, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '经济责任审查'


class PetitionReport(models.Model):
    """信访举报"""
    report_origin_choices = (
        ('省委组织部干部监督机构批转', '省委组织部干部监督机构批转'),
        ('领导批示', '领导批示'),
        ('市本级干部监督机构受理', '市本级干部监督机构受理'),
        ('其他单位转交', '其他单位转交'),
    )
    officer = models.ForeignKey(Officer, verbose_name='干部')
    name = models.CharField('举报人姓名', max_length=10)
    profile = models.CharField('举报人单位及职位', max_length=100)
    report_origin = models.CharField('举报来源', max_length=20,
                                     choices=report_origin_choices,
                                     default='市本级干部监督机构受理')
    content = models.TextField('举报反映的主要问题')
    status = models.TextField('调查情况')
    result = models.TextField('处理意见')
    is_influence = models.CharField(
        '是否影响使用', max_length=4, choices=yes_or_no_choices, blank=True)
    start_time = models.DateField('影响起始时间', null=True, blank=True)
    end_time = models.DateField('影响终止时间', null=True, blank=True)
    origin = models.CharField('信息来源', max_length=20,
                              choices=origin_choices,
                              default='市委组织部')

    def __str__(self):
        return self.officer.name + '-' + self.content

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(PetitionReport, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '信访举报'
        verbose_name_plural = '信访举报事项'


class OrganizeProcess(models.Model):
    """组织处理"""
    status_choices = (
        ('诫勉', '诫勉'),
        ('岗位调整', '岗位调整'),
        ('引咎辞职', '引咎辞职'),
        ('责令辞职', '责令辞职'),
        ('免职', '免职'),
        ('降职', '降职'),
    )
    officer = models.ForeignKey(Officer, verbose_name='干部')
    status = models.CharField('受组织处理情况', max_length=10,
                              choices=status_choices)
    influence = models.CharField('是否影响使用', max_length=5,
                                 choices=yes_or_no_choices,
                                 default='是')
    start_time = models.DateField('影响起始时间')
    end_time = models.DateField('影响终止时间')
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices,
                              default='市委组织部')

    def __str__(self):
        return self.officer.name + '-' + self.status

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(OrganizeProcess, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '组织处理事项'


class PartyAffair(models.Model):
    """纪律处分"""
    officer = models.ForeignKey(Officer, verbose_name='干部')
    affairs_choices = (
        ('党内警告', '党内警告'),
        ('党内严重警告', '党内严重警告'),
        ('撤销党内职务', '撤销党内职务'),
        ('留党察看', '留党察看'),
        ('开除党籍', '开除党籍'),
        ('行政警告', '行政警告'),
        ('行政记过', '行政记过'),
        ('行政记大过', '行政记大过'),
        ('行政降级', '行政降级'),
        ('行政撤职', '行政撤职'),
        ('行政开除', '行政开除'),
    )
    affair = models.CharField(
        '纪律处分', max_length=20,
        choices=affairs_choices, null=True, blank=True)
    is_influence = models.CharField(
        '是否影响使用', max_length=4, choices=yes_or_no_choices, default='是')
    start_time = models.DateField('影响起始时间', null=True, blank=True)
    end_time = models.DateField('影响终止时间', null=True, blank=True)
    origin = models.CharField(
        '信息来源', max_length=10, choices=origin_choices, default='市委组织部')

    def __str__(self):
        return self.officer.name

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(PartyAffair, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '纪律处分'
        verbose_name_plural = '纪律处分'


class VetoAffair(models.Model):
    """一票否决事项"""
    item_choices = (
        ('计生', '计生'),
        ('安全生产', '安全生产'),
        ('信访', '信访'),
    )
    result_choices = (
        ('通报', '通报'),
        ('诫勉', '诫勉'),
        ('党纪处分', '党纪处分'),
        ('政纪处分', '政纪处分'),
    )
    officer = models.ForeignKey(Officer, verbose_name='干部')
    item = models.CharField('被否决事项', max_length=10,
                            choices=item_choices)
    result = models.CharField('处理情况', max_length=10,
                              choices=result_choices)
    is_influence = models.CharField(
        '是否影响使用', max_length=4,
        choices=yes_or_no_choices, default='是', blank=True)
    start_time = models.DateField('影响起始时间', null=True, blank=True)
    end_time = models.DateField('影响终止时间', null=True, blank=True)
    origin = models.CharField(
        '信息来源', max_length=10, choices=origin_choices, default='市委组织部')

    def __str__(self):
        return self.officer.name

    def save(self, *args, **kwargs):
        if (self.officer.forbidden_start is None) or (self.officer.forbidden_start > self.start_time):
            self.officer.forbidden_start = self.start_time
            self.officer.save()
        if (self.officer.forbidden_end is None) or (self.officer.forbidden_end < self.end_time):
            self.officer.forbidden_end = self.end_time
            self.officer.save()
        super(VetoAffair, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '一票否决事项'
