# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models


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
)

yes_or_no_choices = (
    ('是', '是'),
    ('否', '否'),
)


class Officer(models.Model):
    """docstring for Pool."""
    name = models.CharField('姓名', max_length=20)
    pub_date = models.DateTimeField('更新日期')
    gender_choices = (
        ('男', '男'),
        ('女', '女'),
    )
    gender = models.CharField('性别', max_length=2,
                              choices=gender_choices,
                              default='男')
    birthday = models.DateField('出生日期')
    party_time = models.DateField('入党时间')
    job_time = models.DateField('工作时间')
    native = models.CharField('籍贯', max_length=20, default='湖南永州')
    nation = models.CharField('民族', max_length=20, default='汉')
    duty_level = models.CharField('职务层次', max_length=20, default='无')
    id_number = models.CharField('身份证号', max_length=18, default='无')
    job_title = models.CharField('工作单位及职务', max_length=50)
    full_time_edu = models.CharField('全日制学历', max_length=10)
    full_time_deg = models.CharField('全日制学位', max_length=10)
    part_time_edu = models.CharField('在职学历', max_length=10, null=True)
    part_time_deg = models.CharField('在职学位', max_length=10, null=True)
    manage_field = models.CharField('分管工作', max_length=50)
    profile = models.TextField('简历', max_length=1000, null=True)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '是否近期更新?'

    class Meta:
        verbose_name = '干部'
        verbose_name_plural = '干部'


class Choice(models.Model):
    """docstring for Choice."""
    officer = models.ForeignKey(Officer)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.choice


class Assessment(models.Model):
    """考核"""
    officer = models.ForeignKey(Officer)
    year_choices = (
        ('2016', '2016'),
        ('2015', '2015'),
        ('2014', '2014'),
    )
    year = models.CharField('年度', max_length=4,
                            choices=year_choices,
                            default='2017')
    level_choices = (
        ('优秀', '优秀'),
        ('称职', '称职'),
        ('基本称职', '基本称职'),
        ('不称职', '不称职'),
    )
    level = models.CharField('评定等级', max_length=8,
                             choices=level_choices,
                             default='优秀')
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
        ('组织部', '组织部'),
    )
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices)

    def __str__(self):
        return self.year + self.level

    class Meta:
        verbose_name = '年度考核'
        verbose_name_plural = '近三年年度考核'


class PersonalEvent(models.Model):
    """领导干部个人事项报告"""
    officer = models.ForeignKey(Officer)
    index = models.CharField('核查批次', max_length=10)
    status = models.CharField('核查对比情况', max_length=10)
    express = models.TextField('本人说明及提供汇报情况')
    result = models.CharField('处理意见', max_length=20)
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices)

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '领导干部个人事项报告'


class EconomicReview(models.Model):
    """经济责任审查"""
    officer = models.ForeignKey(Officer)
    status = models.TextField('审查基本情况')
    result = models.CharField('处理意见', max_length=20)
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '经济责任审查'


class PetitionReport(models.Model):
    """信访举报"""
    origin_choices = (
        ('省委组织部督办', '省委组织部督办'),
        ('领导批示', '领导批示'),
        ('本市组织部处理', '本市组织部处理'),
        ('其他单位转交', '其他单位转交'),
    )
    petition_choices = (
        ('正处', '正处'),
        ('副处', '副处'),
        ('正科', '正科'),
    )
    officer = models.ForeignKey(Officer)
    name = models.CharField('举报人姓名', max_length=10)
    profile = models.CharField('举报人单位及职位', max_length=100)
    origin = models.CharField('举报来源', max_length=20,
                              choices=origin_choices)
    level = models.CharField('级别', max_length=10,
                             choices=petition_choices)
    content = models.TextField('举报反应主要问题')
    status = models.TextField('核查情况及处理意见')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '信访举报'
        verbose_name_plural = '信访举报事项'


class OrganizeProcess(models.Model):
    """组织处理"""
    status_choices = (
        ('诫勉', '诫勉'),
        ('调整职务', '调整职务'),
        ('引咎辞职', '引咎辞职'),
        ('责令辞职', '责令辞职'),
        ('免职', '免职'),
        ('降职', '降职'),
    )
    officer = models.ForeignKey(Officer)
    status = models.CharField('受组织处理情况', max_length=10,
                              choices=status_choices)
    influence = models.CharField('是否影响使用', max_length=5,
                                 choices=yes_or_no_choices,
                                 default='是')
    start_time = models.DateField('影响起始时间')
    end_time = models.DateField('影响终止时间')
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '组织处理事项'


class PartyAffair(models.Model):
    """党纪、政纪处分"""
    officer = models.ForeignKey(Officer)
    index = models.CharField('核查批次', max_length=10)
    status = models.CharField('核查对比情况', max_length=10)
    express = models.TextField('本人说明及提供汇报情况')
    result = models.CharField('处理意见', max_length=20)
    origin = models.CharField('信息来源', max_length=10,
                              choices=origin_choices)

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = '党纪政纪处分'
        verbose_name_plural = '党纪政纪处分'


class VetoAffair(models.Model):
    """一票否决事项"""
    item_choices = (
        ('计生', '计生'),
        ('安全生产', '安全生产'),
        ('未识别', '未识别'),
        ('信访', '信访'),
    )
    result_choices = (
        ('通报', '通报'),
        ('诫勉', '诫勉'),
        ('党纪处分', '党纪处分'),
        ('政纪处分', '政纪处分'),
    )
    duration_choices = (
        ('半年', '半年'),
        ('一年', '一年'),
        ('两年', '两年'),
    )

    officer = models.ForeignKey(Officer)
    item = models.CharField('被否决事项', max_length=10,
                            choices=item_choices)
    result = models.CharField('处理情况', max_length=10,
                              choices=result_choices)
    duration = models.CharField('影响期限', max_length=10,
                                choices=duration_choices)

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = '事项'
        verbose_name_plural = '一票否决事项'
